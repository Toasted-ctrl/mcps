FROM python:3.12-slim

WORKDIR /app

# Copy only dependency metadata first (layer caching)
COPY pyproject.toml /app/pyproject.toml

# Copy the actual package sources needed for install
COPY shared/ /app/shared/
COPY servers/data_explorer/ /app/servers/data_explorer/

# Install the project (reads deps from pyproject.toml)
RUN pip install --no-cache-dir .

CMD ["python", "-m", "servers.data_explorer.main"]