FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV CHOKIDAR_USEPOLLING=true
ENV WDS_SOCKET_PORT=0

# Expose port
EXPOSE 3000

# Start the app in development mode with hot reloading
CMD ["npm", "start"] 