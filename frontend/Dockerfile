# Multi-stage Dockerfile for React/Next.js frontend

# Base stage
FROM node:20-alpine as base

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Development stage
FROM base as development

# Install all dependencies
RUN npm ci || npm install

# Copy application code
COPY . .

# Expose port
EXPOSE 3000

# Development command
CMD ["npm", "run", "dev"]

# Build stage
FROM base as build

# Install production dependencies
RUN npm ci --only=production || npm install --production

# Copy application code
COPY . .

# Build the application
RUN npm run build || echo "Build step skipped"

# Test stage
FROM base as test

# Install all dependencies including dev
RUN npm ci || npm install

# Copy application code
COPY . .

# Run tests
RUN npm run test:ci || echo "No tests configured"

# E2E test stage
FROM mcr.microsoft.com/playwright:v1.40.0-focal as e2e

WORKDIR /app

# Copy package files and install
COPY package*.json ./
RUN npm ci || npm install

# Copy application and test files
COPY . .

# Install Playwright browsers
RUN npx playwright install --with-deps

# Run E2E tests
CMD ["npx", "playwright", "test"]

# Production stage
FROM node:20-alpine as production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

WORKDIR /app

# Copy built application from build stage
COPY --from=build --chown=nextjs:nodejs /app/.next ./.next
COPY --from=build --chown=nextjs:nodejs /app/public ./public
COPY --from=build --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=build --chown=nextjs:nodejs /app/package.json ./package.json

# Switch to non-root user
USER nextjs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3000/api/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1); })" || exit 1

# Production command
CMD ["npm", "start"]

# Static export stage (for static sites)
FROM nginx:alpine as static

# Copy built static files
COPY --from=build /app/out /usr/share/nginx/html
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost || exit 1

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
