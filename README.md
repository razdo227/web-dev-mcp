# Full Stack Web Dev Toolkit MCP Server

A Model Context Protocol (MCP) server that delivers curated documentation, quickstart commands, and stack guidance for modern full stack web development. Get instant access to setup instructions for popular frameworks, deployment checklists, and personalized stack recommendations—all through your MCP-enabled AI assistant.

## Features

- **Tool Catalog** - Browse 20+ curated web development tools organized by category (runtimes, frameworks, UI libraries, databases, deployment platforms, etc.)
- **Documentation Lookup** - Fetch official docs, summaries, and CLI install commands for any tool in the catalog
- **Framework Quickstart** - Get ready-to-run scaffold commands for Next.js, SvelteKit, Remix, and Nuxt across npm, pnpm, yarn, and bun
- **Stack Recommendations** - Receive opinionated full-stack combinations tailored to your project type, experience level, and realtime requirements
- **Deployment Checklists** - Get step-by-step deployment guides for Vercel, Netlify, and Cloudflare Pages

## Available Tools

The server exposes the following MCP tools:

- `list_tool_categories` - List available categories and their tool members
- `fetch_tool_reference` - Get documentation, install commands, and optional status check for a specific tool
- `framework_quickstart` - Generate starter commands for a framework with your preferred package manager
- `recommend_stack` - Get a personalized stack recommendation based on project description
- `deployment_checklist` - Get deployment steps and notes for a hosting provider

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Usually comes with Python
- **An MCP Client** - Such as:
  - [Claude Desktop](https://claude.ai/download) (recommended)
  - Any MCP-compatible client that supports stdio transport

## Installation & Setup

### Step 1: Clone or Download the Repository

```bash
# If you have git
git clone <your-repo-url> web-dev-mcp
cd web-dev-mcp

# Or download and extract the files to a directory
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
# .venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `mcp[cli]>=1.2.0` - Model Context Protocol SDK
- `httpx>=0.27.0` - Async HTTP client for status checks

### Step 4: Test the Server Locally (Optional)

You can verify the server works by running it directly:

```bash
python fullstack_webdev_server.py
```

The server will start and wait for MCP protocol messages on stdin. You should see log output like:
```
INFO - Starting Full Stack Web Dev MCP server...
```

Press `Ctrl+C` to stop it.

For a more complete test, you can send a protocol handshake:

```bash
printf '%s\n' \
  '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"local-test","version":"0.0.1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python fullstack_webdev_server.py
```

### Step 5: Configure Your MCP Client

#### For Claude Desktop:

1. Open Claude Desktop settings (File > Settings > Developer)
2. Edit your MCP configuration file (usually `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS)
3. Add this server to the `mcpServers` section:

```json
{
  "mcpServers": {
    "fullstack_webdev": {
      "command": "python",
      "args": ["/absolute/path/to/web-dev-mcp/fullstack_webdev_server.py"],
      "env": {
        "FULLSTACK_WEBDEV_DEFAULT_PROVIDER": "vercel"
      }
    }
  }
}
```

**Important:** Replace `/absolute/path/to/web-dev-mcp/` with the actual absolute path to your installation directory.

4. If you're using a virtual environment, you may want to use the venv's Python instead:

```json
{
  "mcpServers": {
    "fullstack_webdev": {
      "command": "/absolute/path/to/web-dev-mcp/.venv/bin/python",
      "args": ["/absolute/path/to/web-dev-mcp/fullstack_webdev_server.py"],
      "env": {
        "FULLSTACK_WEBDEV_DEFAULT_PROVIDER": "vercel"
      }
    }
  }
}
```

5. Restart Claude Desktop

#### For Other MCP Clients:

Configure the server using stdio transport with the command:
```
python /path/to/fullstack_webdev_server.py
```

## Usage Examples

Once configured, you can ask your AI assistant questions like:

- "List all the web development tools you know about"
- "Show me the UI libraries in your catalog"
- "Give me the docs and install steps for Prisma"
- "How do I bootstrap a SvelteKit app with pnpm?"
- "Recommend a stack for a realtime SaaS dashboard"
- "What are the deployment steps for Netlify?"
- "Show me how to set up Next.js with bun"

The server will provide:
- Official documentation links
- CLI installation commands
- Framework scaffolding commands
- Tailored stack recommendations
- Step-by-step deployment guides

## Configuration

### Environment Variables

- `FULLSTACK_WEBDEV_DEFAULT_PROVIDER` (optional)
  - Default deployment provider for checklists
  - Options: `vercel`, `netlify`, `cloudflare pages`
  - Default: `vercel`

No API keys or secrets are required.

## Catalog Coverage

### Runtimes & Package Managers
Node.js, Deno, Bun, npm, pnpm

### App Frameworks
Next.js, SvelteKit, Remix, Nuxt

### UI Libraries & Styling
Tailwind CSS, shadcn/ui

### Animation & 3D
GSAP, Three.js, react-three-fiber

### Databases & ORM
Prisma, Supabase

### Authentication
Auth.js / NextAuth

### Realtime & Messaging
Socket.IO

### Payments & Services
Stripe

### Deployment & Edge
Vercel, Netlify, Cloudflare Pages

### Build Tools & Monorepos
Turborepo

### Testing & Quality
Playwright

### Headless CMS
Sanity

## Architecture

```
MCP Client (e.g., Claude Desktop)
    ↓ (stdio transport)
Full Stack Web Dev Toolkit MCP Server
    ↓ (optional HTTP status checks)
Documentation Sources
```

## Development

### Adding New Tools

1. Open `fullstack_webdev_server.py`
2. Add a new entry to the `RAW_TOOL_DATA` list:

```python
{
    "key": "ToolName",
    "aliases": ["alias1", "alias2"],
    "label": "Tool Name",
    "category": "Category Name",
    "homepage": "https://example.com/docs",
    "summary": "Brief description of the tool",
    "cli": ["npm install tool-name"],
}
```

3. Restart your MCP client to pick up the changes

### Adding New Frameworks

Add entries to `FRAMEWORK_STARTERS` dictionary with quickstart commands for each package manager.

### Adding New Deployment Providers

Add entries to `DEPLOYMENT_PLAYBOOKS` dictionary with steps and notes.

### Adding New Stack Recipes

Add entries to `STACK_RECIPES` list with match keywords, frontend/backend/infrastructure recommendations, and extras.

## Troubleshooting

### Server Not Appearing in Client

- Verify the absolute path in your MCP config is correct
- Check that Python and dependencies are installed
- Look at the MCP client's logs for error messages
- Try running the server manually to check for Python errors

### Tools Not Working

- Ensure you've restarted your MCP client after configuration changes
- Check that the server process is running (look for it in Activity Monitor / Task Manager)
- Review stderr logs for any Python exceptions

### Virtual Environment Issues

If using a venv, make sure:
- You're pointing to the venv's Python in your MCP config
- All dependencies are installed in that venv
- The venv was created with the correct Python version

## Security

- No credentials, API keys, or secrets are required or stored
- All data returned is informational and publicly available
- The server runs with user-level permissions
- HTTP status checks (optional) use a 5-second timeout

## Contributing

Contributions are welcome! To add new tools, frameworks, or deployment providers:

1. Fork the repository
2. Add your changes to the appropriate data structures in `fullstack_webdev_server.py`
3. Test locally using the manual test command
4. Submit a pull request with a description of your additions

## License

MIT License

## Support

For issues, questions, or suggestions:
- Open an issue in the GitHub repository
- Check the MCP documentation at [modelcontextprotocol.io](https://modelcontextprotocol.io/)
- Review the Claude Desktop documentation for MCP setup

## Acknowledgments

Built with:
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic
- [FastMCP](https://github.com/jlowin/fastmcp) SDK
- [httpx](https://www.python-httpx.org/) for async HTTP

---

Happy building! 🚀
