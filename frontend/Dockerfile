FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --no-fund --no-audit

COPY . .

EXPOSE 5173

# Vite dev server is fine for the one-command demo; VITE_API_URL comes from compose.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]