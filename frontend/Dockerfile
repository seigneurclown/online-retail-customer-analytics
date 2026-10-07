# ================================================================
# Multi-stage Dockerfile for React Analytics Platform
# Stage 1: Build production bundle
# Stage 2: Serve via Nginx Alpine with SPA fallback & proxy
# ================================================================

# --- Stage 1: Build ---
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json ./
RUN npm ci

# Copy source files
COPY . .

# Build production bundle with relative API proxy path
ARG VITE_API_BASE_URL=/api/v1
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

RUN npm run build

# --- Stage 2: Serve ---
FROM nginx:alpine

# Remove default nginx configurations
RUN rm -rf /etc/nginx/conf.d/*

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy production build from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -q -O - http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
