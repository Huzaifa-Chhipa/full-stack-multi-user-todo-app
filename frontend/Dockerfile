# Use Node.js 20 as base image
FROM node:20-alpine

# Install dependencies
RUN apk add --no-cache libc6-compat
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci --only=production

# Copy the rest of the application
COPY . .

# Build the Next.js application for production
RUN npm run build

# Expose port
EXPOSE 3000

ENV PORT=3000

# Start the Next.js application in production mode
CMD ["npm", "start"]