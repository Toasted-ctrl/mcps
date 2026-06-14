# Introduction
Hello! This is a general repository with some MCP servers I created. Over time I'll create more MCP servers and upload them here. Feel free to use/copy them!\n
Additionally, this repo contains an "example server", which should assist in rapidly developing a new MCP server from scratch. The example server includes:
- Logging
- Error handling & sanitization
- Prometheus tracking on its own port
# Running an MCP server
## Locally
Navigate to the subdirectory of an MCP from the root directory, for example:
```bash
cd servers/example
```
Rename the .env.example file and add your own variables/credentials:
```bash
mv .env.example .env
nano .env
```
Navigate back to the root directory.
```bash
cd ../..
```
After, to launch, run:
```bash
uv sync
uv run python -m servers.example.main
```
## Docker Compose
navigate to the subdirectory of an MCP from the root directory, for example:
```bash
cd servers/example
```
Rename the .env.example file and add your own variables/credentials:
```bash
mv .env.example .env
nano .env
```
After, run:
```bash
docker compose up
```