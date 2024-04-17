# Use the latest Node.js LTS version as the base image
FROM node:lts

# Set the working directory in the container
WORKDIR /app

# Install P3X Redis UI
RUN npm install -g p3x-redis-ui

# Expose port 7843 (default port used by P3X Redis UI)
EXPOSE 7843

# Start P3X Redis UI when the container starts
CMD ["p3x-redis-ui", "--port", "7843"]