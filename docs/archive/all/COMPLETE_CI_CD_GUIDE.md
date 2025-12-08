Got it — you’d like a **single consolidated master document** that merges the two CI/CD docs you uploaded:

- **CI_CD_GUIDE.md**  
- **CI_MIGRATION_SUMMARY.md**

Here’s a unified version that combines them into one cohesive reference:

---

# CI/CD Pipeline – Master Guide & Migration Summary ✅

**Last Updated:** November 19, 2025  
**Version:** 2.0  
**Maintained By:** DevOps Team / Semour Media Group  

---

## 📌 Table of Contents

1. [Overview](#overview)  
2. [What Changed](#what-changed)  
3. [New Workflow Files](#new-workflow-files)  
4. [CI Pipeline](#ci-pipeline)  
5. [Golden Rules Enforcement](#golden-rules-enforcement)  
6. [Deployment Pipeline](#deployment-pipeline)  
7. [Key Improvements](#key-improvements)  
8. [Migration Checklist](#migration-checklist)  
9. [Required GitHub Secrets](#required-github-secrets)  
10. [Branch Protection Configuration](#branch-protection-configuration)  
11. [Testing the New CI](#testing-the-new-ci)  
12. [Rollback Plan](#rollback-plan)  
13. [Common Issues & Solutions](#common-issues--solutions)  
14. [Performance Optimization](#performance-optimization)  
15. [Monitoring & Alerts](#monitoring--alerts)  
16. [Best Practices](#best-practices)  
17. [Workflow Diagrams](#workflow-diagrams)  
18. [FAQs](#faqs)  
19. [Additional Resources](#additional-resources)  

---

## 1. Overview

The Levelith CI/CD pipeline is designed for **clarity**, **strict enforcement**, and **developer experience**.  

- **Migration Date:** 2025-01-19  
- **Status:** ✅ Ready for production use  
- **Workflows:**  
  1. `ci.yml` – Main CI pipeline  
  2. `golden-rules.yml` – Quality enforcement  
  3. `deploy.yml` – Automated deployment to Render.com  

---

## 2. What Changed

### Old CI System
- 4 overlapping workflow files  
- Hidden failures (`|| true`)  
- No strict enforcement of coverage or docs  
- No automated deployment  

### New CI System
- 3 focused workflows  
- **STRICT enforcement** (coverage ≥80%, docs ≥90%)  
- Clear error messages with fix instructions  
- Automated deployment with health checks  
- PR comments and summaries  

---

## 3. New Workflow Files

### `ci.yml` – Main CI Pipeline
- Backend lint, typecheck, tests (≥80% coverage)  
- Frontend lint, typecheck, tests, build  
- AI agent index validation  
- Runtime: ~5–10 minutes  

### `golden-rules.yml` – Golden Rules Enforcement
- Critical rules: coverage, docs, security, AI index, pinned deps  
- Advisory rules: code quality, performance, commit quality  
- Runtime: ~8–12 minutes  

### `deploy.yml` – Deployment Pipeline
- Pre-deploy checks  
- Build backend + frontend  
- Deploy to Render.com  
- Post-deploy health checks + smoke tests  
- Runtime: ~10–15 minutes  

---

## 4. CI Pipeline

**Triggers:** Push/PR to `main`, `develop`, or `claude/**` branches.  
**Jobs:** Backend + frontend checks, AI index validation.  
**Success Criteria:** All jobs must pass for merge.  
**Failure Handling:** Clear error messages, PR comments.  

---

## 5. Golden Rules Enforcement

**Critical Rules (STRICT):**
1. Test coverage ≥80%  
2. Docstring coverage ≥90%  
3. Security scans (Bandit, Safety, pip-audit, TruffleHog)  
4. AI agent index up to date  
6. Dependencies pinned  

**Advisory Rules:** Code quality, performance, commit format.  

---

## 6. Deployment Pipeline

**Triggers:** After CI + Golden Rules pass on `main`.  
**Stages:** Pre-deploy checks → Build → Deploy → Health checks → Smoke tests.  
**Rollback:** Manual rollback if failure.  

---

## 7. Key Improvements

- Clarity: 3 focused workflows  
- Strict enforcement: no hidden failures  
- Coverage requirement: hard fail <80%  
- Error messages: actionable fixes  
- Deployment: automated with health checks  
- Developer experience: PR comments, summaries  
- Performance: caching + parallel jobs  

---

## 8. Migration Checklist

- [x] Create new workflow files  
- [x] Backup old workflows  
- [x] Update README with badges  
- [x] Add PR template  
- [ ] Configure branch protection rules  
- [ ] Add Render.com secrets  

---

## 9. Required GitHub Secrets

```
RENDER_API_KEY
RENDER_BACKEND_SERVICE_ID
RENDER_FRONTEND_SERVICE_ID
```

Optional: `CODECOV_TOKEN`, `SNYK_TOKEN`, `SLACK_WEBHOOK`.  

---

## 10. Branch Protection Configuration

**Required checks:** CI Success, Golden Rules Summary, Backend Tests, Frontend Build, AI Index.  
**Additional protections:** Require PR reviews, dismiss stale reviews, no force pushes/deletions.  

---

## 11. Testing the New CI

- Create test PR → observe workflows  
- Test failure scenarios (remove test, unformatted code, outdated index)  
- Verify deployment on `main`  

---

## 12. Rollback Plan

Revert to old workflows if critical issues occur:  
```bash
mv ci.yml ci.yml.new
mv golden-rules.yml golden-rules.yml.new
mv deploy.yml deploy.yml.new
mv main-ci.yml.old main-ci.yml
...
```

---

## 13. Common Issues & Solutions

- Coverage below 80% → Add tests  
- AI index out of date → Run `python dev/aiagent_navigator.py index`  
- Code formatting failed → Run `black`, `isort`, `prettier`  
- Unpinned dependencies → Pin versions in requirements.txt  
- Security vulnerabilities → Update packages, rerun scans  
- Deployment failed → Check Render logs, env vars  

---

## 14. Performance Optimization

- **Caching:** pip + npm dependencies  
- **Concurrency:** cancel in-progress runs  
- **Parallelization:** backend + frontend jobs run in parallel  

---

## 15. Monitoring & Alerts

- GitHub Actions dashboard  
- Render dashboard + health endpoints  
- PR comments, GitHub issues, email notifications  

---

## 16. Best Practices

- Run checks locally before pushing  
- Keep PRs small and focused  
- Use conventional commits  
- Maintain ≥80% coverage  
- Keep dependencies up to date  
- Always update AI index after changes  

---

## 17. Workflow Diagrams

### CI Pipeline
```
Push/PR → CI Pipeline
├─ Backend Lint ✓
├─ Backend TypeCheck ✓
├─ Backend Tests (≥80%) ✓
├─ Frontend Lint ✓
├─ Frontend TypeCheck ✓
├─ Frontend Tests ✓
├─ Frontend Build ✓
└─ AI Index ✓
```

### Golden Rules
```
Push/PR → Golden Rules
├─ Tests ≥80% ✅
├─ Docs ≥90% ✅
├─ Security ✅
├─ AI Index ✅
├─ Dependencies ✅
└─ Advisory rules ⚠️
```

### Deployment
```
CI + Golden Rules Pass
   │
   ├─ Pre-Deploy Checks
   ├─ Build Artifacts
   ├─ Deploy Backend + Frontend
   ├─ Health Checks
   └─ Smoke Tests
```

---

## 18. FAQs

- **Why did my PR fail CI?** → Check Actions logs.  
- **Can I skip CI checks?** → No.  
- **How do I test CI changes?** → Create PR.  
- **Can I deploy to staging?** → Yes, via manual dispatch.  
- **How long does CI take?** → ~5–10 minutes.  

---

## 19. Additional Resources

- 📚 [CI/CD Guide](/docs/dev/CI_CD_GUIDE.md)  
- 🏗️ [Deployment Guide](/docs/deployment/RENDER_DEPLOYMENT.md)  
- 🧪 [GitHub Actions Docs](https://docs.github.com/en/actions)  

---

## 🎉 Summary

The migration to the new CI/CD pipeline is complete.  
- ✅ Strict enforcement of quality standards  
- ✅ Automated deployment with health checks  
- ✅ Clear error messages and actionable fixes  
- ✅ Optimized developer experience  

**Status:** Production-ready 🚀  

---

Would you like me to also create a **visual timeline** (Old CI → Migration → New CI/CD → Deployment) so you can present this as a single diagram in your documentation?
