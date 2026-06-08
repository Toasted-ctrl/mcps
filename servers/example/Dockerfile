FROM python:3.12-slim

WORKDIR /app

# Install shared deps first (layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy shared library
COPY shared/ /app/shared/

# Copy this MCP's code
COPY servers/example/ /app/servers/example/

# Set Python path so `from shared.x import y` works
ENV PYTHONPATH=/app

CMD ["python", "-m", "servers.example.main"]