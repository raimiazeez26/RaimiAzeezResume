"""RAI Automations portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="RAI Automations", path="/project/rai-automations", order=36)

layout = lambda: render_project(
    title="RAI Automations",
    category="AI & Automation",
    summary="The operating system for an AI automation agency. A hosted team portal and n8n workflows find prospects, research them with citations, draft tailored outreach for owner approval, and carry approved leads through a sales workspace, all on a PostgreSQL and pgvector memory layer.",
    features=[
        "Discover prospects by area and business type, or research a named business, with rate limits per run and per day.",
        "Show cited research for owner review; approval creates a lead and a price-free outreach draft.",
        "Draft marketing emails that cite the prospect's own website and the agency's documented services.",
        "Manage deals, proposal outlines, and won clients in a sales workspace gated by owner approvals.",
        "Capture conversations and documents into persistent memory with embedding refresh and provenance tracking.",
        "Enforce safeguards on sending: quotas, opt-outs, frozen final messages, and no blind resends.",
    ],
    technologies="Node.js, PostgreSQL, pgvector, n8n, OpenAI, Google OAuth, Docker, Heroku, GitHub Actions",
    repository="https://github.com/raimiazeez26/RAI",
    status="Portal live on Heroku with Google sign-in; prospect discovery and the sales workspace are switched on. Outreach sending is built but switched off pending owner decisions.",
    notes=[
        "Versioned, checksum-checked SQL migrations with unit, fresh-database, and browser tests in CI.",
        "Features ship behind switches so each capability can be enabled in production independently.",
    ],
    private=True,
)
