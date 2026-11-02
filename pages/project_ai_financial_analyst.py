"""AI Financial Analyst portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="AI Financial Analyst", path="/project/ai-financial-analyst", order=32)

layout = lambda: render_project(
    title="AI Financial Analyst Workflow",
    category="AI & Automation",
    summary="An n8n-based financial research pipeline that turns an analyst request into a tracked research job, gathers market data and supporting evidence, runs structured analysis, checks claims, prepares a report, and records processing history.",
    features=[
        "Accept research requests from Telegram and webhook entry points.",
        "Retrieve market and fundamentals data and calculate deterministic metrics.",
        "Separate evidence retrieval, specialist analysis, verification, and report generation into workflow stages.",
        "Deliver research results and retain job, verification, and audit records with PostgreSQL support.",
        "Provide grounded follow-up Q&A against stored research context.",
    ],
    technologies="n8n, OpenAI, Python, yfinance, PostgreSQL, Telegram, webhooks",
    repository="https://github.com/raimiazeez26/ai-financial-analyst",
    status="Workflow exports are available in the repository; the README identifies evidence retrieval as a testing stub that needs live document sources before production use.",
    notes=[
        "The verification workflow is designed to classify outputs as verified, review required, or rejected.",
        "Use fictional sample requests when trying the public bot demo; do not submit sensitive personal or financial data.",
    ],
)
