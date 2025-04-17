FROM python:3.11-alpine

# Install system dependencies for Pillow
RUN apk add --no-cache jpeg-dev zlib-dev libjpeg

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server.py .

# Make the script executable
RUN chmod +x server.py

# Run the MCP server
CMD ["python", "server.py"] 