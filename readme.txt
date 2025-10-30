# Full Stack Web Dev Toolkit MCP Server

A Model Context Protocol (MCP) server that delivers curated documentation, quickstart commands, and stack guidance for modern full stack web development.

## Purpose

This MCP server provides a secure interface for AI assistants to answer build-time questions, suggest stacks, and surface installation steps for the most popular frameworks, runtimes, and deployment providers.

## Features

### Current Implementation
- **`list_tool_categories`** - Expands the curated catalog by category to reveal available tooling.
- **`fetch_tool_reference`** - Returns official documentation links, summaries, and CLI install commands for any tool in the catalog.
- **`framework_quickstart`** - Supplies ready-to-run project scaffolding commands across npm, pnpm, yarn, and bun.
- **`recommend_stack`** - Suggests an opinionated full-stack combination tailored to project goals, experience level, and realtime needs.
- **`deployment_checklist`** - Produces hosting-specific deployment steps and reminders for Vercel, Netlify, and Cloudflare Pages.

## Prerequisites

- Docker Desktop with MCP Toolkit enabled
- Docker MCP CLI plugin (`docker mcp` command)
- Internet access during runtime for optional documentation status checks

## Installation

See the step-by-step instructions provided with the files.

## Usage Examples

In Claude Desktop or any MCP-aware client, you can ask:

- "List the UI libraries you have info on."
- "Give me the docs and install steps for Prisma."
- "How do I bootstrap a Remix app with pnpm?"
- "Recommend a stack for a realtime SaaS dashboard for a small team."
- "What are the deployment steps for Cloudflare Pages?"

## Architecture

```
Claude Desktop → MCP Gateway → Full Stack Web Dev Toolkit MCP Server → Documentation Sources
↓
Docker Desktop Secrets
(No secrets required)
```

## Development

### Local Testing

```bash
# (Optional) set defaults for provider hints
export FULLSTACK_WEBDEV_DEFAULT_PROVIDER=vercel

# Install deps (recommended to use a venv)
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Run directly (server waits for an MCP client over stdio)
python fullstack_webdev_server.py

# Minimal protocol smoke test (initialize handshake + list tools)
printf '%s\n' \
  '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"local-test","version":"0.0.1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python fullstack_webdev_server.py
```

### Adding New Tools

1. Add the function to `fullstack_webdev_server.py`
2. Decorate with `@mcp.tool()`
3. Update the catalog entry with the new tool name
4. Rebuild the Docker image

## Troubleshooting

### Tools Not Appearing
- Verify Docker image built successfully
- Check catalog and registry files
- Ensure the MCP gateway config references the custom catalog
- Restart the MCP client

### Authentication Errors
- No secrets are required; ensure environment variables are optional

## Security Considerations

- No credentials are stored or required
- Running as non-root user inside Docker
- Only informational data is returned; no sensitive data is logged

## License

MIT License
