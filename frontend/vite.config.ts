import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@/components': path.resolve(__dirname, './src/components'),
      '@/lib': path.resolve(__dirname, './src/lib'),
      '@/hooks': path.resolve(__dirname, './src/hooks'),
      '@/admin': path.resolve(__dirname, './src/admin'),
      '@/admin/features': path.resolve(__dirname, './src/admin/features'),
      '@/admin/components': path.resolve(__dirname, './src/admin/components'),
      '@/admin/lib': path.resolve(__dirname, './src/admin/lib'),
      '@/admin/hooks': path.resolve(__dirname, './src/admin/hooks'),
      '@/admin/types': path.resolve(__dirname, './src/admin/types'),
    },
  },
  base: process.env.VITE_BASE_PATH || '/',
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: process.env.VITE_API_URL || 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'query-vendor': ['@tanstack/react-query', '@tanstack/react-table'],
          'form-vendor': ['react-hook-form', '@hookform/resolvers', 'zod'],
          'ui-vendor': [
            '@radix-ui/react-dialog',
            '@radix-ui/react-dropdown-menu',
            '@radix-ui/react-select',
            '@radix-ui/react-toast',
            '@radix-ui/react-label',
          ],
        },
      },
    },
  },
});
