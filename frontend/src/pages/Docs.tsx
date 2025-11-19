/**
 * Docs Page - Wiki-style documentation viewer
 * Dynamically displays markdown documentation with sidebar navigation
 * Uses ONETRUTH configuration for all styling
 */

import React, { useState, useEffect } from 'react';
import { Link, useParams, useNavigate } from 'react-router-dom';
import { ONETRUTH } from '../config/ONETRUTH';

interface DocItem {
  path: string;
  title: string;
  category: string;
}

const Docs: React.FC = () => {
  const { docPath } = useParams<{ docPath?: string }>();
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
  const [docContent, setDocContent] = useState<string>('');
  const [sidebarExpanded, setSidebarExpanded] = useState(true);

  // Documentation structure - maps to /docs folder
  const documentation: DocItem[] = [
    // Core Documentation
    { path: 'README', title: 'Documentation Index', category: 'Core' },
    { path: 'core/MANIFEST', title: 'Project Manifest', category: 'Core' },
    { path: 'core/AI_AGENT_GOLDEN_RULES', title: 'AI Agent Golden Rules', category: 'Core' },
    { path: 'core/KNOWN_ISSUES', title: 'Known Issues', category: 'Core' },

    // Development
    { path: 'dev/DEVELOPMENT_PRIORITIES', title: 'Development Priorities', category: 'Development' },
    { path: 'dev/CODEBASE_ANALYSIS', title: 'Codebase Analysis', category: 'Development' },
    { path: 'dev/AI_AGENT_TOOLING', title: 'AI Agent Tooling', category: 'Development' },
    { path: 'dev/ADMIN_PANEL_GUIDE', title: 'Admin Panel Guide', category: 'Development' },
    { path: 'dev/NAICS_IMPORT_GUIDE', title: 'NAICS Import Guide', category: 'Development' },
    { path: 'dev/NAICS_QUICK_REFERENCE', title: 'NAICS Quick Reference', category: 'Development' },
    { path: 'dev/NAVIGATION', title: 'Navigation Guide', category: 'Development' },
    { path: 'dev/TEST_REPORT', title: 'Test Report', category: 'Development' },
    { path: 'dev/COMPREHENSIVE_TODO_REPORT', title: 'Todo Report', category: 'Development' },

    // API Documentation
    { path: 'api/API_DOCUMENTATION', title: 'API Documentation', category: 'API' },

    // Backend
    { path: 'backend/NAICS_EXPANSION_SUMMARY', title: 'NAICS Expansion Summary', category: 'Backend' },
  ];

  // Group docs by category
  const groupedDocs = documentation.reduce((acc, doc) => {
    if (!acc[doc.category]) {
      acc[doc.category] = [];
    }
    acc[doc.category].push(doc);
    return acc;
  }, {} as Record<string, DocItem[]>);

  // Filter docs based on search
  const filteredDocs = documentation.filter(doc =>
    doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    doc.path.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    if (docPath) {
      setSelectedDoc(docPath);
      loadDocContent(docPath);
    } else if (!selectedDoc && documentation.length > 0) {
      // Default to README
      setSelectedDoc('README');
      loadDocContent('README');
    }
  }, [docPath]);

  const loadDocContent = async (path: string) => {
    try {
      // In production, this would fetch from an API endpoint
      // For now, we'll use placeholder content
      setDocContent(`# ${path}\n\nLoading documentation for: ${path}\n\nThis documentation viewer will fetch markdown content from the /docs folder via the backend API.`);
    } catch (error) {
      setDocContent(`# Error\n\nFailed to load documentation: ${path}`);
    }
  };

  const handleDocSelect = (path: string) => {
    setSelectedDoc(path);
    loadDocContent(path);
    navigate(`/docs/${path}`);
  };

  const styles = {
    container: {
      display: 'flex',
      height: '100vh',
      backgroundColor: ONETRUTH.colors.background,
    },
    sidebar: {
      width: sidebarExpanded ? '320px' : '60px',
      backgroundColor: ONETRUTH.colors.surfaceDark,
      color: ONETRUTH.colors.textInverse,
      padding: sidebarExpanded ? ONETRUTH.spacing.lg : ONETRUTH.spacing.sm,
      overflowY: 'auto' as const,
      transition: `width ${ONETRUTH.transitions.base}`,
      boxShadow: ONETRUTH.shadows.lg,
    },
    sidebarHeader: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      marginBottom: ONETRUTH.spacing.lg,
    },
    logo: {
      fontSize: ONETRUTH.fonts.sizes['2xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      display: sidebarExpanded ? 'block' : 'none',
    },
    toggleButton: {
      background: 'transparent',
      border: 'none',
      color: ONETRUTH.colors.textInverse,
      fontSize: ONETRUTH.fonts.sizes.xl,
      cursor: 'pointer',
      padding: ONETRUTH.spacing.sm,
    },
    searchBox: {
      width: '100%',
      padding: ONETRUTH.spacing.sm,
      marginBottom: ONETRUTH.spacing.lg,
      borderRadius: ONETRUTH.borderRadius.md,
      border: `1px solid ${ONETRUTH.colors.border}`,
      fontSize: ONETRUTH.fonts.sizes.sm,
      backgroundColor: ONETRUTH.colors.surface,
      display: sidebarExpanded ? 'block' : 'none',
    },
    category: {
      marginBottom: ONETRUTH.spacing.lg,
      display: sidebarExpanded ? 'block' : 'none',
    },
    categoryTitle: {
      fontSize: ONETRUTH.fonts.sizes.sm,
      fontWeight: ONETRUTH.fonts.weights.semibold,
      color: ONETRUTH.colors.primary,
      textTransform: 'uppercase' as const,
      marginBottom: ONETRUTH.spacing.sm,
      letterSpacing: '0.05em',
    },
    docItem: {
      padding: ONETRUTH.spacing.sm,
      marginBottom: ONETRUTH.spacing.xs,
      borderRadius: ONETRUTH.borderRadius.sm,
      cursor: 'pointer',
      transition: `all ${ONETRUTH.transitions.fast}`,
      fontSize: ONETRUTH.fonts.sizes.sm,
      color: ONETRUTH.colors.textInverse,
    },
    docItemActive: {
      backgroundColor: ONETRUTH.colors.primary,
      fontWeight: ONETRUTH.fonts.weights.semibold,
    },
    docItemHover: {
      backgroundColor: 'rgba(52, 152, 219, 0.2)',
    },
    content: {
      flex: 1,
      padding: ONETRUTH.spacing['2xl'],
      overflowY: 'auto' as const,
      backgroundColor: ONETRUTH.colors.surface,
    },
    contentHeader: {
      marginBottom: ONETRUTH.spacing.xl,
      paddingBottom: ONETRUTH.spacing.lg,
      borderBottom: `2px solid ${ONETRUTH.colors.border}`,
    },
    backLink: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: ONETRUTH.spacing.sm,
      color: ONETRUTH.colors.primary,
      fontSize: ONETRUTH.fonts.sizes.base,
      fontWeight: ONETRUTH.fonts.weights.medium,
      marginBottom: ONETRUTH.spacing.md,
      cursor: 'pointer',
    },
    contentTitle: {
      fontSize: ONETRUTH.fonts.sizes['4xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      color: ONETRUTH.colors.textDark,
    },
    markdown: {
      fontSize: ONETRUTH.fonts.sizes.base,
      lineHeight: ONETRUTH.fonts.lineHeights.relaxed,
      color: ONETRUTH.colors.text,
    },
  };

  return (
    <div style={styles.container}>
      {/* Sidebar */}
      <aside style={styles.sidebar}>
        <div style={styles.sidebarHeader}>
          <Link to="/" style={styles.logo}>Levelith</Link>
          <button
            style={styles.toggleButton}
            onClick={() => setSidebarExpanded(!sidebarExpanded)}
            aria-label="Toggle sidebar"
          >
            {sidebarExpanded ? '◀' : '▶'}
          </button>
        </div>

        {sidebarExpanded && (
          <>
            <input
              type="text"
              placeholder="Search documentation..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={styles.searchBox}
            />

            {searchTerm ? (
              <div style={styles.category}>
                <div style={styles.categoryTitle}>Search Results</div>
                {filteredDocs.map((doc) => (
                  <div
                    key={doc.path}
                    style={{
                      ...styles.docItem,
                      ...(selectedDoc === doc.path ? styles.docItemActive : {}),
                    }}
                    onClick={() => handleDocSelect(doc.path)}
                    onMouseOver={(e) => {
                      if (selectedDoc !== doc.path) {
                        e.currentTarget.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
                      }
                    }}
                    onMouseOut={(e) => {
                      if (selectedDoc !== doc.path) {
                        e.currentTarget.style.backgroundColor = 'transparent';
                      }
                    }}
                  >
                    {doc.title}
                  </div>
                ))}
              </div>
            ) : (
              Object.entries(groupedDocs).map(([category, docs]) => (
                <div key={category} style={styles.category}>
                  <div style={styles.categoryTitle}>{category}</div>
                  {docs.map((doc) => (
                    <div
                      key={doc.path}
                      style={{
                        ...styles.docItem,
                        ...(selectedDoc === doc.path ? styles.docItemActive : {}),
                      }}
                      onClick={() => handleDocSelect(doc.path)}
                      onMouseOver={(e) => {
                        if (selectedDoc !== doc.path) {
                          e.currentTarget.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
                        }
                      }}
                      onMouseOut={(e) => {
                        if (selectedDoc !== doc.path) {
                          e.currentTarget.style.backgroundColor = 'transparent';
                        }
                      }}
                    >
                      {doc.title}
                    </div>
                  ))}
                </div>
              ))
            )}
          </>
        )}
      </aside>

      {/* Content */}
      <main style={styles.content}>
        <div style={styles.contentHeader}>
          <Link to="/" style={styles.backLink}>
            ← Back to Home
          </Link>
          <h1 style={styles.contentTitle}>
            {documentation.find(d => d.path === selectedDoc)?.title || 'Documentation'}
          </h1>
        </div>

        <div style={styles.markdown}>
          <pre style={{ whiteSpace: 'pre-wrap', fontFamily: ONETRUTH.fonts.body }}>
            {docContent}
          </pre>
        </div>
      </main>
    </div>
  );
};

export default Docs;
