"""Boardroom AI v2 portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="Boardroom AI v2", path="/project/boardroom-ai", order=35)

layout = lambda: render_project(
    title="Boardroom AI v2",
    category="AI & Automation",
    summary="An evidence-grounded AI assistant built with n8n, PostgreSQL, and pgvector. It turns approved company documents into a searchable knowledge base, answers questions through Telegram and web endpoints, verifies each claim against retrieved evidence, and escalates uncertain requests for human review.",
    features=[
        "Synchronise approved Google Drive folders, then chunk, embed, and index documents in pgvector.",
        "Classify intent first, routing small talk, unclear, out-of-scope, and handoff requests away from retrieval.",
        "Answer company questions with a specialist agent that retrieves evidence filtered by the user's access level.",
        "Verify generated claims against the retrieved evidence and label the sources behind every answer.",
        "Fail safely: unsupported answers go to human review and missing knowledge goes to a customer-agent handoff.",
        "Record conversations, messages, and audit events in PostgreSQL.",
    ],
    technologies="n8n, PostgreSQL, pgvector, Google Drive, large language models, Telegram Bot API, Web API",
    repository="https://github.com/raimiazeez26/boardroom-ai-v2",
    status="Published workflow architecture with SQL migrations and a public Telegram demo bot (t.me/boardroom_ai_advisor_v2_bot).",
    notes=[
        "Use fictional questions in the demo; do not submit confidential company data.",
        "Builds on Boardroom AI v1, a supervisor-and-specialist advisory bot, adding retrieval, verification, and access control.",
    ],
)
