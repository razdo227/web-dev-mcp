#!/usr/bin/env python3
"""
Simple Full Stack Web Dev MCP Server - curated docs and stack guidance.
"""
import os
import sys
import logging
from datetime import datetime, timezone

import httpx
from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("fullstack-webdev-server")

mcp = FastMCP("fullstack_webdev")

DEFAULT_PROVIDER = os.environ.get("FULLSTACK_WEBDEV_DEFAULT_PROVIDER", "vercel")


def _normalize_key(value: str) -> str:
    """Normalize lookup keys."""
    return value.strip().lower()


RAW_TOOL_DATA = [
    {
        "key": "Node.js",
        "aliases": ["node", "nodejs"],
        "label": "Node.js",
        "category": "Core Runtimes & Package Managers",
        "homepage": "https://nodejs.org/en/docs",
        "summary": "JavaScript runtime built on Chrome V8, foundational for most tooling in this catalog.",
        "cli": [
            "curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -",
            "sudo apt-get install -y nodejs",
        ],
    },
    {
        "key": "Deno",
        "aliases": [],
        "label": "Deno",
        "category": "Core Runtimes & Package Managers",
        "homepage": "https://docs.deno.com/runtime/",
        "summary": "Secure JavaScript runtime with built-in tooling, TypeScript, and Web APIs.",
        "cli": ["curl -fsSL https://deno.land/install.sh | sh"],
    },
    {
        "key": "Bun",
        "aliases": [],
        "label": "Bun",
        "category": "Core Runtimes & Package Managers",
        "homepage": "https://bun.com/docs",
        "summary": "High-performance JavaScript runtime with fast bundler, transpiler, and test runner.",
        "cli": ["curl -fsSL https://bun.sh/install | bash"],
    },
    {
        "key": "npm",
        "aliases": [],
        "label": "npm",
        "category": "Core Runtimes & Package Managers",
        "homepage": "https://nodejs.org/api/all.html",
        "summary": "Default Node.js package manager and registry client.",
        "cli": ["npm install -g npm@latest"],
    },
    {
        "key": "pnpm",
        "aliases": [],
        "label": "pnpm",
        "category": "Core Runtimes & Package Managers",
        "homepage": "https://pnpm.io",
        "summary": "Fast disk-efficient JavaScript package manager with monorepo tooling.",
        "cli": ["npm install -g pnpm"],
    },
    {
        "key": "Next.js",
        "aliases": ["next"],
        "label": "Next.js",
        "category": "App Frameworks",
        "homepage": "https://nextjs.org/docs/app/getting-started",
        "summary": "React framework for hybrid SSR/SSG apps with App Router and server actions.",
        "cli": ["npx create-next-app@latest"],
    },
    {
        "key": "SvelteKit",
        "aliases": ["sveltekit"],
        "label": "SvelteKit",
        "category": "App Frameworks",
        "homepage": "https://svelte.dev/docs/kit",
        "summary": "Full-stack application framework for Svelte with filesystem routing and adapters.",
        "cli": ["npm create svelte@latest my-app"],
    },
    {
        "key": "Remix",
        "aliases": [],
        "label": "Remix",
        "category": "App Frameworks",
        "homepage": "https://remix.run/docs",
        "summary": "Web-native full stack framework focusing on nested routes and progressive enhancement.",
        "cli": ["npx create-remix@latest"],
    },
    {
        "key": "Tailwind CSS",
        "aliases": ["tailwind"],
        "label": "Tailwind CSS",
        "category": "UI Libraries & Styling",
        "homepage": "https://tailwindcss.com/docs",
        "summary": "Utility-first CSS framework with design system friendly primitives.",
        "cli": ["npm install -D tailwindcss postcss autoprefixer"],
    },
    {
        "key": "shadcn/ui",
        "aliases": ["shadcn"],
        "label": "shadcn/ui",
        "category": "UI Libraries & Styling",
        "homepage": "https://ui.shadcn.com/docs/installation",
        "summary": "Copy-and-paste React component library built on Radix primitives and Tailwind.",
        "cli": ["npx shadcn@latest init"],
    },
    {
        "key": "GSAP",
        "aliases": [],
        "label": "GSAP",
        "category": "Animation & Motion",
        "homepage": "https://gsap.com/docs/v3/",
        "summary": "Robust animation platform for high-performance timeline and scroll effects.",
        "cli": ["npm install gsap"],
    },
    {
        "key": "Three.js",
        "aliases": ["three"],
        "label": "Three.js",
        "category": "WebGL / 3D / Shader Libraries",
        "homepage": "https://threejs.org/docs/",
        "summary": "Popular WebGL library for 3D graphics, scenes, and shaders in the browser.",
        "cli": ["npm install three"],
    },
    {
        "key": "react-three-fiber",
        "aliases": ["r3f"],
        "label": "react-three-fiber",
        "category": "WebGL / 3D / Shader Libraries",
        "homepage": "https://r3f.docs.pmnd.rs/getting-started/introduction",
        "summary": "React renderer for Three.js enabling declarative 3D scenes.",
        "cli": ["npm install @react-three/fiber three"],
    },
    {
        "key": "Prisma",
        "aliases": [],
        "label": "Prisma",
        "category": "Databases, ORM & Storage",
        "homepage": "https://www.prisma.io/docs",
        "summary": "Type-safe ORM with migrations, schema, and database tooling.",
        "cli": ["npm install prisma --save-dev", "npx prisma init"],
    },
    {
        "key": "Supabase",
        "aliases": [],
        "label": "Supabase",
        "category": "Databases, ORM & Storage",
        "homepage": "https://supabase.com/docs",
        "summary": "Open source Firebase alternative with Postgres, auth, storage, and realtime APIs.",
        "cli": ["npm install @supabase/supabase-js"],
    },
    {
        "key": "Auth.js",
        "aliases": ["nextauth"],
        "label": "Auth.js / NextAuth",
        "category": "Authentication",
        "homepage": "https://next-auth.js.org/",
        "summary": "Authentication toolkit for Next.js and other runtimes with provider ecosystem.",
        "cli": ["npm install next-auth"],
    },
    {
        "key": "Socket.IO",
        "aliases": ["socketio"],
        "label": "Socket.IO",
        "category": "Realtime & Messaging",
        "homepage": "https://socket.io/docs/v4",
        "summary": "Realtime bidirectional communication library with WebSocket fallback handling.",
        "cli": ["npm install socket.io"],
    },
    {
        "key": "Stripe",
        "aliases": [],
        "label": "Stripe",
        "category": "Payments, Email & Analytics",
        "homepage": "https://stripe.com/docs",
        "summary": "Payments platform with billing, invoicing, and checkout APIs.",
        "cli": ["npm install stripe"],
    },
    {
        "key": "Vercel",
        "aliases": [],
        "label": "Vercel",
        "category": "Deployment & Edge",
        "homepage": "https://vercel.com/docs",
        "summary": "Serverless platform for frontend frameworks, previews, and edge functions.",
        "cli": ["npm install -g vercel"],
    },
    {
        "key": "Netlify",
        "aliases": [],
        "label": "Netlify",
        "category": "Deployment & Edge",
        "homepage": "https://docs.netlify.com/",
        "summary": "Jamstack deployment platform with build pipelines and serverless functions.",
        "cli": ["npm install -g netlify-cli"],
    },
    {
        "key": "Turborepo",
        "aliases": [],
        "label": "Turborepo",
        "category": "Build Tools & Monorepos",
        "homepage": "https://turbo.build/repo/docs",
        "summary": "High-performance build system for JavaScript and TypeScript monorepos.",
        "cli": ["npm install turbo --save-dev"],
    },
    {
        "key": "Playwright",
        "aliases": [],
        "label": "Playwright",
        "category": "Testing, Linting & Quality",
        "homepage": "https://playwright.dev/",
        "summary": "End-to-end testing framework for modern web apps with browser automation.",
        "cli": ["npm init playwright@latest"],
    },
    {
        "key": "Sanity",
        "aliases": [],
        "label": "Sanity",
        "category": "Headless CMS & Content",
        "homepage": "https://www.sanity.io/docs",
        "summary": "Composable content platform with real-time collaboration and GROQ queries.",
        "cli": ["npm create sanity@latest"],
    },
]

TOOL_LOOKUP = {}
CATEGORY_LOOKUP = {}

for entry in RAW_TOOL_DATA:
    normalized = _normalize_key(entry["key"])
    TOOL_LOOKUP[normalized] = entry
    for alias in entry["aliases"]:
        TOOL_LOOKUP[_normalize_key(alias)] = entry
    category = entry["category"]
    CATEGORY_LOOKUP.setdefault(category, []).append(entry["label"])

FRAMEWORK_STARTERS = {
    "next.js": {
        "label": "Next.js",
        "docs": "https://nextjs.org/docs/app/getting-started",
        "commands": {
            "npm": "npx create-next-app@latest my-app",
            "pnpm": "pnpm create next-app my-app",
            "yarn": "yarn create next-app my-app",
            "bun": "bun create next-app my-app",
        },
        "post": [
            "cd my-app",
            "npm run dev",
            "Open http://localhost:3000",
        ],
    },
    "sveltekit": {
        "label": "SvelteKit",
        "docs": "https://svelte.dev/docs/kit",
        "commands": {
            "npm": "npm create svelte@latest my-app",
            "pnpm": "pnpm create svelte@latest my-app",
            "yarn": "yarn create svelte@latest my-app",
            "bun": "bun create svelte@latest my-app",
        },
        "post": [
            "cd my-app",
            "npm install",
            "npm run dev -- --open",
        ],
    },
    "remix": {
        "label": "Remix",
        "docs": "https://remix.run/docs/en/main/start/quickstart",
        "commands": {
            "npm": "npx create-remix@latest",
            "pnpm": "pnpm create remix",
            "yarn": "yarn create remix",
            "bun": "bun create remix",
        },
        "post": [
            "cd my-remix-app",
            "npm run dev",
        ],
    },
    "nuxt": {
        "label": "Nuxt",
        "docs": "https://nuxt.com/docs/getting-started/installation",
        "commands": {
            "npm": "npx nuxi@latest init my-app",
            "pnpm": "pnpm dlx nuxi@latest init my-app",
            "yarn": "yarn dlx nuxi@latest init my-app",
            "bun": "bunx nuxi@latest init my-app",
        },
        "post": [
            "cd my-app",
            "npm install",
            "npm run dev -- --open",
        ],
    },
}

DEPLOYMENT_PLAYBOOKS = {
    "vercel": {
        "label": "Vercel",
        "docs": "https://vercel.com/docs/deployments/overview",
        "steps": [
            "Install CLI: npm install -g vercel",
            "Login: vercel login",
            "Link project: vercel link",
            "Create preview: vercel --prod false",
            "Promote to production: vercel deploy --prod",
        ],
        "notes": [
            "Git integrations auto-build previews per PR.",
            "Edge functions and serverless functions deploy automatically.",
        ],
    },
    "netlify": {
        "label": "Netlify",
        "docs": "https://docs.netlify.com/site-deploys/create-deploys/",
        "steps": [
            "Install CLI: npm install -g netlify-cli",
            "Login: netlify login",
            "Init project: netlify init",
            "Configure build: netlify sites:update --build-command 'npm run build'",
            "Deploy preview: netlify deploy --build",
        ],
        "notes": [
            "Use netlify deploy --prod to publish production builds.",
            "Netlify functions can live in netlify/functions directory.",
        ],
    },
    "cloudflare pages": {
        "label": "Cloudflare Pages",
        "docs": "https://developers.cloudflare.com/pages/",
        "steps": [
            "Install wrangler: npm install -g wrangler",
            "Login: wrangler login",
            "Initialize: wrangler pages project create",
            "Deploy preview: wrangler pages deploy dist",
            "Promote: wrangler pages deploy dist --branch=main",
        ],
        "notes": [
            "Supports full-stack with Pages Functions.",
            "Edge rendering requires wrangler.toml configuration.",
        ],
    },
}

STACK_RECIPES = [
    {
        "id": "content-marketing",
        "match": ["landing", "marketing", "content", "portfolio"],
        "summary": "High-performance marketing site with strong content authoring.",
        "frontend": "Next.js + Tailwind CSS + shadcn/ui",
        "backend": "Sanity CMS via GROQ queries",
        "infrastructure": "Deploy to Vercel with on-demand ISR",
        "extras": ["Use Plausible for lightweight analytics", "Leverage Framer Motion for hero animations"],
    },
    {
        "id": "saas-dashboard",
        "match": ["saas", "dashboard", "b2b", "admin"],
        "summary": "Full-stack SaaS template with auth, database, and realtime features.",
        "frontend": "Next.js App Router with TanStack Query",
        "backend": "Prisma ORM set up against Postgres (Neon or Supabase)",
        "infrastructure": "Deploy API routes on Vercel, run background tasks on Vercel Cron",
        "extras": ["Stripe billing portal integration", "Use Socket.IO for live metrics if realtime=yes"],
    },
    {
        "id": "creative-studio",
        "match": ["3d", "animation", "creative", "studio"],
        "summary": "Visually rich experience with 3D and smooth motion.",
        "frontend": "SvelteKit with Three.js or react-three-fiber via Svelte bindings",
        "backend": "Supabase for data and storage",
        "infrastructure": "Deploy to Netlify for fine-grained edge routing",
        "extras": ["Use GSAP ScrollTrigger for parallax sections", "Optimize assets with Cloudinary"],
    },
    {
        "id": "commerce",
        "match": ["shop", "commerce", "ecommerce", "store"],
        "summary": "Commerce-ready stack with payments and CMS-driven catalog.",
        "frontend": "Next.js + Tailwind CSS + Radix Primitives",
        "backend": "Payload CMS or Sanity for catalog with webhook-driven revalidation",
        "infrastructure": "Deploy to Vercel or Netlify, connect Stripe for checkout",
        "extras": ["Use Auth.js for customer sessions", "Add LogRocket for session replay"],
    },
]


def _format_timestamp() -> str:
    """Return current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@mcp.tool()
async def list_tool_categories(category: str = "") -> str:
    """List available tool categories and members."""
    logger.info("Listing tool categories for category=%s", category)
    if category.strip():
        normalized = _normalize_key(category)
        matched = None
        for key in CATEGORY_LOOKUP:
            if _normalize_key(key) == normalized:
                matched = key
                break
        if not matched:
            return f"❌ Error: Unknown category '{category}'."
        tools = sorted(CATEGORY_LOOKUP.get(matched, []))
        items = "\n".join(f"- {tool}" for tool in tools)
        return f"""📊 Category: {matched}

Tools:
{items}

Timestamp: {_format_timestamp()}"""

    overview_lines = []
    for cat, tools in sorted(CATEGORY_LOOKUP.items()):
        overview_lines.append(f"- {cat} ({len(tools)} tools)")
    content = "\n".join(overview_lines)
    return f"""📁 Available Categories:
{content}

Tip: Pass category=\"{next(iter(CATEGORY_LOOKUP))}\" to expand a category."""


@mcp.tool()
async def fetch_tool_reference(tool: str = "", include_status: str = "") -> str:
    """Retrieve documentation details for a tooling name."""
    logger.info("Fetching tool reference for tool=%s include_status=%s", tool, include_status)
    if not tool.strip():
        return "❌ Error: Tool name is required."
    normalized = _normalize_key(tool)
    entry = TOOL_LOOKUP.get(normalized)
    if not entry:
        return f"❌ Error: Tool '{tool}' is not in the curated catalog."

    status_line = ""
    if include_status.strip().lower() in {"1", "true", "yes"}:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.head(entry["homepage"])
                status_line = f"🌐 Status: {response.status_code} {response.reason_phrase}"
        except httpx.HTTPStatusError as exc:
            status_line = f"❌ HTTP Error: {exc.response.status_code}"
        except Exception as exc:
            status_line = f"⚠️ Status Check Failed: {str(exc)}"

    cli_lines = "\n".join(f"- {cmd}" for cmd in entry["cli"])
    result = f"""✅ {entry['label']} ({entry['category']})
Summary: {entry['summary']}
Docs: {entry['homepage']}
CLI Setup:
{cli_lines}"""
    if status_line:
        result = f"{result}\n{status_line}"
    return result


@mcp.tool()
async def framework_quickstart(framework: str = "", package_manager: str = "") -> str:
    """Provide quickstart commands for a framework."""
    logger.info("Providing quickstart for framework=%s package_manager=%s", framework, package_manager)
    if not framework.strip():
        return "❌ Error: Framework name is required."
    normalized = _normalize_key(framework)
    starter = FRAMEWORK_STARTERS.get(normalized)
    if not starter:
        return f"❌ Error: Framework '{framework}' is not supported."
    pm = package_manager.strip().lower() if package_manager.strip() else "npm"
    command = starter["commands"].get(pm)
    if not command:
        available = ", ".join(starter["commands"].keys())
        return f"❌ Error: Package manager '{package_manager}' not supported. Try one of: {available}."
    post_lines = "\n".join(f"- {step}" for step in starter["post"])
    return f"""⚡ {starter['label']} Quickstart
Command: {command}
Next Steps:
{post_lines}
Docs: {starter['docs']}"""


@mcp.tool()
async def recommend_stack(project: str = "", experience: str = "", realtime: str = "") -> str:
    """Suggest a full-stack combination for a project."""
    logger.info("Recommending stack for project=%s experience=%s realtime=%s", project, experience, realtime)
    if not project.strip():
        return "❌ Error: Provide a brief project description."
    project_tokens = {_normalize_key(token) for token in project.split()}
    realtime_enabled = realtime.strip().lower() in {"yes", "true", "1", "enabled"}
    experience_level = experience.strip().lower() if experience.strip() else "intermediate"

    chosen = None
    for recipe in STACK_RECIPES:
        if any(term in project_tokens for term in recipe["match"]):
            chosen = recipe
            break
    if not chosen:
        chosen = {
            "summary": "General purpose full-stack setup suitable for most product MVPs.",
            "frontend": "Next.js + Tailwind CSS + Radix Primitives",
            "backend": "Prisma with a hosted Postgres (Neon) via Supabase connection pooling",
            "infrastructure": "Deploy frontend and server actions on Vercel; use Turborepo if monorepo grows.",
            "extras": [
                "Add Auth.js for authentication flows",
                "Add Stripe or Resend depending on payments or email needs",
            ],
        }

    extras = list(chosen.get("extras", []))
    if realtime_enabled and "Socket.IO" not in " ".join(extras):
        extras.append("Integrate Socket.IO or Ably for realtime features")
    if experience_level in {"beginner", "junior"}:
        extras.append("Prioritize npm scripts and avoid complex monorepo setups initially")
    elif experience_level in {"senior", "expert"}:
        extras.append("Consider Turborepo with pnpm workspaces for scalable builds")

    extras_lines = "\n".join(f"- {item}" for item in extras)
    return f"""✅ Recommended Stack
Summary: {chosen['summary']}
Frontend: {chosen['frontend']}
Backend: {chosen['backend']}
Infrastructure: {chosen['infrastructure']}
Extras:
{extras_lines}"""


@mcp.tool()
async def deployment_checklist(provider: str = "", preview: str = "") -> str:
    """Return deployment checklist for a hosting provider."""
    selected = provider.strip().lower() if provider.strip() else DEFAULT_PROVIDER
    logger.info("Fetching deployment checklist for provider=%s preview=%s", selected, preview)
    entry = DEPLOYMENT_PLAYBOOKS.get(selected)
    if not entry and selected == DEFAULT_PROVIDER:
        entry = DEPLOYMENT_PLAYBOOKS.get("vercel")
    if not entry:
        options = ", ".join(sorted(DEPLOYMENT_PLAYBOOKS.keys()))
        return f"❌ Error: Unknown provider '{provider}'. Supported providers: {options}."
    steps = "\n".join(f"- {step}" for step in entry["steps"])
    notes = "\n".join(f"- {note}" for note in entry["notes"])
    preview_hint = ""
    if preview.strip().lower() in {"yes", "true", "1"}:
        preview_hint = "\nPreview Mode: Enable preview deployments by linking feature branches."
    return f"""🚀 {entry['label']} Deployment Checklist
Docs: {entry['docs']}
Steps:
{steps}
Notes:
{notes}{preview_hint}"""


if __name__ == "__main__":
    logger.info("Starting Full Stack Web Dev MCP server...")
    try:
        mcp.run(transport="stdio")
    except Exception as exc:
        logger.error("Server error: %s", exc, exc_info=True)
        sys.exit(1)
