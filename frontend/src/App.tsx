/**
 * Main App Component - Levelith Frontend
 *
 * Routes:
 * - / : Landing page
 * - /docs/* : Documentation wiki
 * - /admin/* : Admin dashboard
 */

import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Docs from './pages/Docs_old';
import AdminApp from './admin/App';
import { DataSourceProvider } from './admin/context/DataSourceContext';

const App: React.FC = () => {
  return (
    <Routes>
      {/* Main landing page */}
      <Route path="/" element={<Landing />} />

      {/* Documentation wiki - supports nested paths like core/MANIFEST */}
      <Route path="/docs" element={<Docs />} />
      <Route path="/docs/*" element={<Docs />} />

      {/* Admin dashboard - wrapped in DataSourceProvider */}
      <Route
        path="/admin/*"
        element={
          <DataSourceProvider>
            <AdminApp />
          </DataSourceProvider>
        }
      />
    </Routes>
  );
};

export default App;
