# Security Considerations
These MCP servers expose system and container-level metrics over HTTP with no authentication or encryption by default. Please review the following recommendations before deploying to any environment.
## Firewall Rules
Restrict access to MCP ports so only your chat client can reach each MCP. For example, using `ufw`:
```bash
# On each node — allow only the control server to scrape
sudo ufw allow from <CHAT_CLIENT_IP> to any port <MCP_PORT>
sudo ufw allow from <PROMETHEUS_CLIENT_IP> to any port <MCP_PROMETHEUS_PORT>
sudo ufw deny <MCP_PORT>
sudo ufw deny <MCP_PROMETHEUS_PORT>
```
## Use a Private Network or VPN
Whenever possible, run all monitoring traffic over a private management network or a VPN (e.g., WireGuard, Tailscale). Avoid scraping metrics over the public internet.