# Full Stack Web Dev Toolkit MCP Server

## Overview
- **Server name**: `fullstack_webdev`
- **Entry point**: `fullstack_webdev_server.py`
- **Purpose**: Serve curated documentation, quickstart commands, and deployment checklists for modern full stack web development tools.

## Available Tools
- `list_tool_categories` – Enumerate catalog categories and their tool members.
- `fetch_tool_reference` – Fetch summary, docs link, install commands, and optional HTTP status for a specific tool.
- `framework_quickstart` – Generate starter commands for Next.js, SvelteKit, Remix, or Nuxt across npm, pnpm, yarn, and bun.
- `recommend_stack` – Propose a stack based on project description, experience level, and realtime needs.
- `deployment_checklist` – Output opinionated deployment steps and notes for Vercel, Netlify, or Cloudflare Pages.

## Configuration
- Optional environment variable: `FULLSTACK_WEBDEV_DEFAULT_PROVIDER` (defaults to `vercel`).
- No API keys or secrets are required; any secrets block in catalogs can be omitted.

## Operational Notes
- All logging is routed to stderr via Python `logging`.
- HTTP status checks use `httpx.AsyncClient().head()` with a 5-second timeout.
- Outputs use emoji markers for clarity while remaining plaintext-friendly.

## Testing
Install dependencies first (e.g., `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`).
```bash
python fullstack_webdev_server.py
printf '%s\n' \
  '{"jsonrpc":"2.0","id":0,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"local-test","version":"0.0.1"}}}' \
  '{"jsonrpc":"2.0","method":"notifications/initialized","params":{}}' \
  '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' \
  | python fullstack_webdev_server.py
```

## Extending
- Append new tool metadata in `RAW_TOOL_DATA`.
- Add quickstart metadata in `FRAMEWORK_STARTERS` or deployment details in `DEPLOYMENT_PLAYBOOKS`.
- Construct new MCP tools by following the existing pattern: sanitize input via `.strip()`, log intent, handle errors, and return formatted strings only.
