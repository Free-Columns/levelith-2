"""
Neural Hive Service

Integrates the "Truth-as-a-Service" pipeline for transforming unstructured
journal entries into standardized Experience Objects.
"""

import json
import uuid
import re
from typing import List, Dict, Optional
from datetime import datetime

from openai import OpenAI
from pinecone import Pinecone

from backend.config import settings
from backend.models.experience import ExperienceCategory, ExperienceType

class NeuralHiveService:
    def __init__(self):
        # Initialize clients using settings
        self.openai_client = OpenAI(api_key=settings.openai_api_key)
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.pc.Index(settings.pinecone_index_name)

    # --- AGENT 1: SCRIBE (The Parser) ---
    def _parse_journal(self, journal_text: str) -> Dict:
        """Scribe-Alpha: Splits text into atomic activities."""
        system_prompt = """
        You are Scribe-Alpha. Convert raw user journal entries into structured 'Proto-Activities'.
        
        RULES:
        1. Split distinct activities (e.g., "I coded then had a meeting" -> 2 activities).
        2. Identify Duration (minutes). Estimate if missing.
        3. Identify URLs as 'evidence_url'.
        4. Determine Concurrency: 'PRIMARY' (Active/Stamina Cost) vs 'SECONDARY' (Passive).
        
        OUTPUT JSON:
        {
            "activities": [
                {
                    "description": "Action text",
                    "duration_minutes": 120,
                    "type": "PRIMARY" | "SECONDARY",
                    "evidence_url": "http..." or null
                }
            ]
        }
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": journal_text}
                ],
                temperature=0.0
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"Scribe Error: {e}")
            return {"activities": []}

    # --- AGENT 2: CLASSIFIER (The Bureaucrat) ---
    def _get_embedding(self, text: str) -> List[float]:
        response = self.openai_client.embeddings.create(
            input=text.replace("\n", " "),
            model="text-embedding-3-small"
        )
        return response.data[0].embedding

    def _search_pinecone(self, vector: List[float], namespace: str, top_k: int = 5):
        results = self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            namespace=namespace
        )
        context_str = ""
        matches = []
        for match in results['matches']:
            meta = match['metadata']
            matches.append({
                "id": match['id'],
                "score": match['score'],
                "text": meta.get('text_context', ''),
                "metadata": meta
            })
            context_str += f"ID: {match['id']} | DETAILS: {meta.get('text_context', '')[:500]}...\n\n"
        return context_str, matches

    def _classify_activity(self, activity_desc: str) -> Optional[Dict]:
        """Classifier-X: Maps activity to NAICS/O*NET codes."""
        # 1. Embed
        vector = self._get_embedding(activity_desc)
        
        # 2. RAG Search
        naics_ctx, naics_matches = self._search_pinecone(vector, settings.namespace_naics)
        onet_ctx, onet_matches = self._search_pinecone(vector, settings.namespace_onet)
        
        # 3. LLM Decision
        system_prompt = """
        You are Classifier-X. Map the activity to the BEST NAICS and O*NET code.
        
        RETURN JSON:
        {
            "naics_id": "ID of chosen NAICS candidate",
            "onet_id": "ID of chosen O*NET candidate",
            "category": "WORKPLACE" | "EDUCATION" | "SKILLS"
        }
        """
        
        user_prompt = f"""
        ACTIVITY: "{activity_desc}"
        NAICS OPTIONS: {naics_ctx}
        ONET OPTIONS: {onet_ctx}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            decision = json.loads(response.choices[0].message.content)
            
            # Hydrate with full data
            return {
                "decision": decision,
                "onet_data": next((m for m in onet_matches if m['id'] == decision.get('onet_id')), None),
                "naics_data": next((m for m in naics_matches if m['id'] == decision.get('naics_id')), None)
            }
        except Exception as e:
            print(f"Classifier Error: {e}")
            return None

    # --- AGENT 3: SHERLOCK (The Builder) ---
    def _build_experience_object(self, user_id: str, proto_act: Dict, classification: Dict) -> Dict:
        """Sherlock: Assembles the final object."""
        decision = classification['decision']
        onet = classification['onet_data']
        naics = classification['naics_data']

        # Extract Skills Snapshot from O*NET text
        skills = []
        if onet:
            text = onet.get('text', '')
            match = re.search(r"Tasks: (.*?)(?=\. Tools:|\.$)", text, re.IGNORECASE)
            if match:
                skills = [t.strip() for t in match.group(1).split(',') if t.strip()]

        # Map to Levelith Categories (Basic Mapping)
        category_map = {
            "WORKPLACE": ExperienceCategory.WORKPLACE.value,
            "EDUCATION": ExperienceCategory.EDUCATION.value,
            "SKILLS": ExperienceCategory.SKILLS.value
        }
        
        # Determine Experience Type (Simplified logic for MVP)
        # In a real app, you might infer GIG vs FULL_TIME based on duration/context
        exp_type = ExperienceType.GIG.value if decision.get('category') == 'WORKPLACE' else ExperienceType.COURSE.value

        return {
            "title": onet['metadata']['title'] if onet else proto_act['description'],
            "description": proto_act['description'],
            "naics_code": naics['metadata']['code'] if naics else "123456",
            "category": category_map.get(decision.get('category'), ExperienceCategory.WORKPLACE.value),
            "experience_type": exp_type,
            "start_date": datetime.utcnow().isoformat(),
            "skills_gained": skills,
            "metadata": {
                "neural_hive_id": str(uuid.uuid4()),
                "onet_code": onet['metadata']['code'] if onet else None,
                "duration_minutes": proto_act['duration_minutes'],
                "evidence_url": proto_act.get('evidence_url')
            }
        }

    # --- MAIN PIPELINE ---
    def process_journal_entry(self, user_id: str, journal_text: str) -> List[Dict]:
        """
        Main entry point: Pipeline that runs Scribe -> Classifier -> Sherlock.
        Returns a list of potential Experience objects (dicts) ready for review or saving.
        """
        # 1. Parse
        parsed = self._parse_journal(journal_text)
        results = []

        # 2. Loop & Classify
        for act in parsed.get('activities', []):
            classification = self._classify_activity(act['description'])
            if classification:
                # 3. Build
                xo = self._build_experience_object(user_id, act, classification)
                results.append(xo)
        
        return results