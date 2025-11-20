/**
 * Docs Page - Wiki-style documentation viewer
 * Dynamically displays markdown documentation with hierarchical sidebar navigation
 * Supports 4-level deep folder structure with breadcrumb navigation
 * Uses ONETRUTH configuration for all styling
 */

import React, { useState, useEffect, useCallback } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeRaw from 'rehype-raw';
import rehypeHighlight from 'rehype-highlight';
import { ONETRUTH } from '../config/ONETRUTH';
import 'highlight.js/styles/github-dark.css';

interface DocFile {
  type: 'file';
  name: string;
  title: string;
  path: string;
  filename: string;
}

interface DocFolder {
  type: 'folder';
  name: string;
  path: string;
  children: (DocFile | DocFolder)[];
}

type DocItem = DocFile | DocFolder;

const Docs: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  // Extract the doc path from URL - everything after /docs/
  // e.g., /docs/agent/MANIFEST -> agent/MANIFEST
  const docPath = location.pathname.startsWith('/docs/')
    ? location.pathname.slice(6) // Remove '/docs/' prefix
    : undefined;
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDoc, setSelectedDoc] = useState<string | null>(null);
  const [docContent, setDocContent] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [sidebarExpanded, setSidebarExpanded] = useState(true);
  const [docStructure, setDocStructure] = useState<DocItem[]>([]);
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(new Set());

  // Fetch documentation structure from backend
  useEffect(() => {
    const fetchDocList = async () => {
      try {
        const apiUrl = import.meta.env.VITE_API_URL || 'https://levelith-backend.onrender.com/api/v1';
        const response = await fetch(`${apiUrl}/docs/list`);

        if (!response.ok) {
          throw new Error('Failed to fetch documentation list');
        }

        const data = await response.json();
        setDocStructure(data.structure || []);

        // Auto-expand first level folders
        const firstLevelPaths = new Set<string>();
        data.structure?.forEach((item: DocItem) => {
          if (item.type === 'folder') {
            firstLevelPaths.add(item.path);
          }
        });
        setExpandedFolders(firstLevelPaths);
      } catch (error) {
        console.error('Error fetching documentation list:', error);
        setDocStructure([]);
      }
    };

    fetchDocList();
  }, []);

  // Toggle folder expansion
  const toggleFolder = (path: string) => {
    setExpandedFolders(prev => {
      const newSet = new Set(prev);
      if (newSet.has(path)) {
        newSet.delete(path);
      } else {
        newSet.add(path);
      }
      return newSet;
    });
  };

  // Find all files for search
  const findAllFiles = (items: DocItem[]): DocFile[] => {
    const files: DocFile[] = [];
    items.forEach(item => {
      if (item.type === 'file') {
        files.push(item);
      } else {
        files.push(...findAllFiles(item.children));
      }
    });
    return files;
  };

  const allFiles = findAllFiles(docStructure);

  // Filter docs based on search
  const filteredDocs = searchTerm
    ? allFiles.filter(doc =>
        doc.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.path?.toLowerCase().includes(searchTerm.toLowerCase())
      )
    : [];

  const loadDocContent = useCallback(async (path: string) => {
    setIsLoading(true);
    setError(null);

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'https://levelith-backend.onrender.com/api/v1';
      const response = await fetch(`${apiUrl}/docs/${path}`);

      if (!response.ok) {
        throw new Error(`Failed to load documentation: ${response.statusText}`);
      }

      const markdown = await response.text();
      setDocContent(markdown);
    } catch (error) {
      console.error('Error loading documentation:', error);
      setError(error instanceof Error ? error.message : 'Failed to load documentation');
      setDocContent('# Error\n\nFailed to load documentation. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (docPath) {
      // URL has a specific doc path - load it and expand parent folders
      setSelectedDoc(docPath);
      loadDocContent(docPath);

      // Auto-expand all parent folders
      const pathParts = docPath.split('/');
      const newExpanded = new Set(expandedFolders);
      for (let i = 1; i <= pathParts.length; i++) {
        newExpanded.add(pathParts.slice(0, i).join('/'));
      }
      setExpandedFolders(newExpanded);
    } else if (docStructure.length > 0 && !docContent) {
      // No doc path in URL and no content loaded yet - load default README
      const defaultDoc = 'README';
      setSelectedDoc(defaultDoc);
      loadDocContent(defaultDoc);
      navigate(`/docs/${defaultDoc}`, { replace: true });
    }
  }, [docPath, docStructure.length, docContent, loadDocContent, navigate]);

  const handleDocSelect = (path: string) => {
    setSelectedDoc(path);
    loadDocContent(path);
    navigate(`/docs/${path}`);
  };

  // Generate breadcrumb from path
  const generateBreadcrumbs = (path: string): { label: string; path: string }[] => {
    if (!path) return [];

    const parts = path.split('/');
    const breadcrumbs: { label: string; path: string }[] = [];

    for (let i = 0; i < parts.length; i++) {
      const partPath = parts.slice(0, i + 1).join('/');
      const label = parts[i].replace(/_/g, ' ').replace(/-/g, ' ');
      breadcrumbs.push({
        label: label.charAt(0).toUpperCase() + label.slice(1),
        path: partPath,
      });
    }

    return breadcrumbs;
  };

  // Render a single navigation item (file or folder)
  const renderNavItem = (item: DocItem, depth: number = 0): React.ReactNode => {
    const indentStyle = {
      paddingLeft: `${depth * 16 + 8}px`,
    };

    if (item.type === 'file') {
      return (
        <div
          key={item.path}
          style={{
            ...styles.docItem,
            ...indentStyle,
            ...(selectedDoc === item.path ? styles.docItemActive : {}),
          }}
          onClick={() => handleDocSelect(item.path)}
          onMouseOver={(e) => {
            if (selectedDoc !== item.path) {
              e.currentTarget.style.backgroundColor = 'rgba(52, 152, 219, 0.2)';
            }
          }}
          onMouseOut={(e) => {
            if (selectedDoc !== item.path) {
              e.currentTarget.style.backgroundColor = 'transparent';
            }
          }}
        >
          📄 {item.title}
        </div>
      );
    } else {
      const isExpanded = expandedFolders.has(item.path);
      return (
        <div key={item.path}>
          <div
            style={{
              ...styles.folderItem,
              ...indentStyle,
            }}
            onClick={() => toggleFolder(item.path)}
          >
            <span style={{ marginRight: '6px' }}>{isExpanded ? '📂' : '📁'}</span>
            <span>{item.name}</span>
          </div>
          {isExpanded && (
            <div>
              {item.children.map(child => renderNavItem(child, depth + 1))}
            </div>
          )}
        </div>
      );
    }
  };

  const styles = {
    container: {
      display: 'flex',
      height: '100vh',
      backgroundColor: ONETRUTH.colors.background,
      fontFamily: ONETRUTH.fonts.body,
    },
    sidebar: {
      width: sidebarExpanded ? '320px' : '60px',
      backgroundColor: ONETRUTH.colors.surfaceDark,
      color: ONETRUTH.colors.textInverse,
      padding: sidebarExpanded ? ONETRUTH.spacing.lg : ONETRUTH.spacing.sm,
      overflowY: 'auto' as const,
      transition: `width ${ONETRUTH.transitions.base}`,
      boxShadow: ONETRUTH.shadows.lg,
      flexShrink: 0,
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
      color: ONETRUTH.colors.textInverse,
      textDecoration: 'none',
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
    navContainer: {
      display: sidebarExpanded ? 'block' : 'none',
    },
    folderItem: {
      padding: ONETRUTH.spacing.sm,
      marginBottom: ONETRUTH.spacing.xs,
      borderRadius: ONETRUTH.borderRadius.sm,
      cursor: 'pointer',
      transition: `all ${ONETRUTH.transitions.fast}`,
      fontSize: ONETRUTH.fonts.sizes.sm,
      color: ONETRUTH.colors.textInverse,
      fontWeight: ONETRUTH.fonts.weights.medium,
      display: 'flex',
      alignItems: 'center',
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
    content: {
      flex: 1,
      padding: ONETRUTH.spacing['2xl'],
      overflowY: 'auto' as const,
      backgroundColor: ONETRUTH.colors.surface,
      maxWidth: '100%',
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
      textDecoration: 'none',
    },
    breadcrumbs: {
      display: 'flex',
      alignItems: 'center',
      gap: ONETRUTH.spacing.xs,
      marginBottom: ONETRUTH.spacing.md,
      fontSize: ONETRUTH.fonts.sizes.sm,
      color: ONETRUTH.colors.text,
      flexWrap: 'wrap' as const,
    },
    breadcrumbItem: {
      color: ONETRUTH.colors.primary,
      cursor: 'pointer',
      textDecoration: 'none',
    },
    breadcrumbSeparator: {
      color: ONETRUTH.colors.textLight,
      margin: `0 ${ONETRUTH.spacing.xs}`,
    },
    breadcrumbCurrent: {
      color: ONETRUTH.colors.textDark,
      fontWeight: ONETRUTH.fonts.weights.semibold,
    },
    contentTitle: {
      fontSize: ONETRUTH.fonts.sizes['4xl'],
      fontFamily: ONETRUTH.fonts.heading,
      fontWeight: ONETRUTH.fonts.weights.bold,
      color: ONETRUTH.colors.textDark,
      marginTop: ONETRUTH.spacing.md,
    },
    loadingSpinner: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '300px',
      fontSize: ONETRUTH.fonts.sizes.xl,
      color: ONETRUTH.colors.primary,
    },
    errorBox: {
      backgroundColor: ONETRUTH.colors.error,
      color: 'white',
      padding: ONETRUTH.spacing.lg,
      borderRadius: ONETRUTH.borderRadius.md,
      marginBottom: ONETRUTH.spacing.lg,
    },
    searchResults: {
      marginBottom: ONETRUTH.spacing.lg,
    },
    searchResultsTitle: {
      fontSize: ONETRUTH.fonts.sizes.sm,
      fontWeight: ONETRUTH.fonts.weights.semibold,
      color: ONETRUTH.colors.primary,
      textTransform: 'uppercase' as const,
      marginBottom: ONETRUTH.spacing.sm,
      letterSpacing: '0.05em',
    },
  };

  // Custom markdown styles using ONETRUTH
  const markdownStyles = `
    .markdown-content {
      font-family: ${ONETRUTH.fonts.body};
      font-size: ${ONETRUTH.fonts.sizes.base};
      line-height: ${ONETRUTH.fonts.lineHeights.relaxed};
      color: ${ONETRUTH.colors.text};
      max-width: 100%;
      overflow-wrap: break-word;
    }

    .markdown-content h1 {
      font-family: ${ONETRUTH.fonts.heading};
      font-size: ${ONETRUTH.fonts.sizes['3xl']};
      font-weight: ${ONETRUTH.fonts.weights.bold};
      color: ${ONETRUTH.colors.textDark};
      margin-top: ${ONETRUTH.spacing.xl};
      margin-bottom: ${ONETRUTH.spacing.lg};
      border-bottom: 2px solid ${ONETRUTH.colors.border};
      padding-bottom: ${ONETRUTH.spacing.sm};
    }

    .markdown-content h2 {
      font-family: ${ONETRUTH.fonts.heading};
      font-size: ${ONETRUTH.fonts.sizes['2xl']};
      font-weight: ${ONETRUTH.fonts.weights.bold};
      color: ${ONETRUTH.colors.textDark};
      margin-top: ${ONETRUTH.spacing.lg};
      margin-bottom: ${ONETRUTH.spacing.md};
    }

    .markdown-content h3 {
      font-family: ${ONETRUTH.fonts.heading};
      font-size: ${ONETRUTH.fonts.sizes.xl};
      font-weight: ${ONETRUTH.fonts.weights.semibold};
      color: ${ONETRUTH.colors.textDark};
      margin-top: ${ONETRUTH.spacing.md};
      margin-bottom: ${ONETRUTH.spacing.sm};
    }

    .markdown-content h4 {
      font-size: ${ONETRUTH.fonts.sizes.lg};
      font-weight: ${ONETRUTH.fonts.weights.semibold};
      color: ${ONETRUTH.colors.textDark};
      margin-top: ${ONETRUTH.spacing.md};
      margin-bottom: ${ONETRUTH.spacing.sm};
    }

    .markdown-content p {
      margin-bottom: ${ONETRUTH.spacing.md};
      line-height: ${ONETRUTH.fonts.lineHeights.relaxed};
    }

    .markdown-content a {
      color: ${ONETRUTH.colors.linkText};
      text-decoration: underline;
      transition: color ${ONETRUTH.transitions.fast};
    }

    .markdown-content a:hover {
      color: ${ONETRUTH.colors.linkHover};
    }

    .markdown-content code {
      background-color: ${ONETRUTH.colors.codeBackground};
      padding: 2px 6px;
      border-radius: ${ONETRUTH.borderRadius.sm};
      font-family: ${ONETRUTH.fonts.monospace};
      font-size: ${ONETRUTH.fonts.sizes.sm};
      color: ${ONETRUTH.colors.codeText};
    }

    .markdown-content pre {
      background-color: ${ONETRUTH.colors.codeBlockBackground};
      color: ${ONETRUTH.colors.codeBlockText};
      padding: ${ONETRUTH.spacing.lg};
      border-radius: ${ONETRUTH.borderRadius.md};
      overflow-x: auto;
      margin-bottom: ${ONETRUTH.spacing.lg};
      box-shadow: ${ONETRUTH.shadows.sm};
    }

    .markdown-content pre code {
      background-color: transparent;
      padding: 0;
      color: inherit;
      font-size: ${ONETRUTH.fonts.sizes.sm};
    }

    /* Ensure syntax highlighting from highlight.js is visible */
    .markdown-content pre code .hljs {
      color: inherit;
    }

    /* Override any conflicting highlight.js colors for better visibility */
    .markdown-content pre .hljs-comment,
    .markdown-content pre .hljs-quote {
      color: #95a5a6;
    }

    .markdown-content pre .hljs-keyword,
    .markdown-content pre .hljs-selector-tag,
    .markdown-content pre .hljs-tag {
      color: #3498db;
    }

    .markdown-content pre .hljs-string,
    .markdown-content pre .hljs-attr,
    .markdown-content pre .hljs-attribute {
      color: #2ecc71;
    }

    .markdown-content pre .hljs-number,
    .markdown-content pre .hljs-literal {
      color: #e67e22;
    }

    .markdown-content pre .hljs-built_in,
    .markdown-content pre .hljs-builtin-name {
      color: #9b59b6;
    }

    .markdown-content ul, .markdown-content ol {
      margin-bottom: ${ONETRUTH.spacing.md};
      padding-left: ${ONETRUTH.spacing.xl};
    }

    .markdown-content li {
      margin-bottom: ${ONETRUTH.spacing.xs};
    }

    .markdown-content blockquote {
      border-left: 4px solid ${ONETRUTH.colors.blockquoteBorder};
      padding-left: ${ONETRUTH.spacing.lg};
      margin-left: 0;
      margin-bottom: ${ONETRUTH.spacing.md};
      color: ${ONETRUTH.colors.blockquoteText};
      font-style: italic;
      background-color: ${ONETRUTH.colors.blockquoteBackground};
      padding: ${ONETRUTH.spacing.md} ${ONETRUTH.spacing.lg};
      border-radius: ${ONETRUTH.borderRadius.sm};
    }

    .markdown-content table {
      width: 100%;
      border-collapse: collapse;
      margin-bottom: ${ONETRUTH.spacing.lg};
      overflow-x: auto;
      display: block;
    }

    .markdown-content thead {
      background-color: ${ONETRUTH.colors.tableHeaderBackground};
    }

    .markdown-content th {
      padding: ${ONETRUTH.spacing.sm} ${ONETRUTH.spacing.md};
      text-align: left;
      font-weight: ${ONETRUTH.fonts.weights.semibold};
      border: 1px solid ${ONETRUTH.colors.border};
      color: ${ONETRUTH.colors.tableHeaderText};
    }

    .markdown-content td {
      padding: ${ONETRUTH.spacing.sm} ${ONETRUTH.spacing.md};
      border: 1px solid ${ONETRUTH.colors.border};
    }

    .markdown-content tr:nth-child(even) {
      background-color: ${ONETRUTH.colors.tableRowEven};
    }

    .markdown-content hr {
      border: none;
      border-top: 2px solid ${ONETRUTH.colors.border};
      margin: ${ONETRUTH.spacing.xl} 0;
    }

    .markdown-content img {
      max-width: 100%;
      height: auto;
      border-radius: ${ONETRUTH.borderRadius.md};
      margin: ${ONETRUTH.spacing.md} 0;
    }

    .markdown-content strong {
      font-weight: ${ONETRUTH.fonts.weights.bold};
      color: ${ONETRUTH.colors.textDark};
    }

    .markdown-content em {
      font-style: italic;
    }
  `;

  const breadcrumbs = selectedDoc ? generateBreadcrumbs(selectedDoc) : [];
  const selectedFile = selectedDoc ? allFiles.find(f => f.path === selectedDoc) : null;

  return (
    <>
      <style>{markdownStyles}</style>
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

              <div style={styles.navContainer}>
                {searchTerm ? (
                  <div style={styles.searchResults}>
                    <div style={styles.searchResultsTitle}>Search Results ({filteredDocs.length})</div>
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
                        📄 {doc.title}
                        <div style={{ fontSize: '11px', color: ONETRUTH.colors.textLight, marginTop: '2px' }}>
                          {doc.path}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  docStructure.map(item => renderNavItem(item, 0))
                )}
              </div>
            </>
          )}
        </aside>

        {/* Content */}
        <main style={styles.content}>
          <div style={styles.contentHeader}>
            <Link to="/" style={styles.backLink}>
              ← Back to Home
            </Link>

            {/* Breadcrumbs */}
            {breadcrumbs.length > 0 && (
              <div style={styles.breadcrumbs}>
                <Link to="/docs/README" style={styles.breadcrumbItem}>📚 Docs</Link>
                {breadcrumbs.map((crumb, index) => (
                  <React.Fragment key={crumb.path}>
                    <span style={styles.breadcrumbSeparator}>/</span>
                    {index === breadcrumbs.length - 1 ? (
                      <span style={styles.breadcrumbCurrent}>{crumb.label}</span>
                    ) : (
                      <a
                        href={`/docs/${crumb.path}`}
                        style={styles.breadcrumbItem}
                        onClick={(e) => {
                          e.preventDefault();
                          handleDocSelect(crumb.path);
                        }}
                      >
                        {crumb.label}
                      </a>
                    )}
                  </React.Fragment>
                ))}
              </div>
            )}

            <h1 style={styles.contentTitle}>
              {selectedFile?.title || 'Documentation'}
            </h1>
          </div>

          {error && (
            <div style={styles.errorBox}>
              <strong>Error:</strong> {error}
            </div>
          )}

          {isLoading ? (
            <div style={styles.loadingSpinner}>
              Loading documentation...
            </div>
          ) : (
            <div className="markdown-content">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw, rehypeHighlight]}
                components={{
                  a: ({ node, children, href, ...props }) => {
                    // Remove .md extension from both link text and href
                    const linkText = typeof children[0] === 'string' ? children[0] : '';
                    const cleanedText = linkText.endsWith('.md') ? linkText.slice(0, -3) : linkText;

                    // Clean the href - remove .md extension and convert to proper /docs/ URL
                    let cleanedHref = href;
                    if (href && !href.startsWith('http') && !href.startsWith('#')) {
                      // Internal doc link
                      cleanedHref = href.endsWith('.md') ? href.slice(0, -3) : href;
                      // If it doesn't start with /, make it relative to /docs/
                      if (!cleanedHref.startsWith('/')) {
                        cleanedHref = `/docs/${cleanedHref}`;
                      }
                    }

                    return <a {...props} href={cleanedHref}>{cleanedText || children}</a>;
                  },
                }}
              >
                {docContent}
              </ReactMarkdown>
            </div>
          )}
        </main>
      </div>
    </>
  );
};

export default Docs;
