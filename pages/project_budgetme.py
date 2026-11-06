"""BudgetMe portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="BudgetMe", path="/project/budgetme", order=34)

layout = lambda: render_project(
    title="BudgetMe",
    category="Data Science & Analytics",
    summary="A personal finance web application for signing in, organizing monthly budgets, and reviewing spending summaries. The React interface includes budget dashboards, chart components, account flows, and a yearly overview.",
    features=[
        "Provide signup, login, password recovery, and protected app routes.",
        "Organize monthly budget items and display summary charts.",
        "Offer a yearly overview and settings area for the authenticated user.",
        "Connect the frontend to Supabase for authentication and application data.",
    ],
    technologies="React, TypeScript, Vite, Supabase, Recharts, Tailwind CSS, shadcn/ui",
    repository="https://github.com/raimiazeez26/BudgetMe",
    status="Frontend application source is available; a working deployment requires valid Supabase project configuration and database setup.",
    notes=["Supabase credentials belong in local environment configuration and should not be committed to the portfolio repository."],
    private=True,
)
