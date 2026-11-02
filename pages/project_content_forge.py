"""Content Forge portfolio overview."""
import dash
from .project_detail import render_project

dash.register_page(__name__, name="Content Forge", path="/project/content-forge", order=31)

layout = lambda: render_project(
    title="Content Forge",
    category="AI & Automation",
    summary="A local rendering service for branded social content. It accepts prepared copy and creates vertical image or short silent video assets, with HTTP endpoints that can be called from automation workflows.",
    features=[
        "Render 1080 × 1920 branded PNG posters from structured content payloads.",
        "Convert posters into 720 × 1280 silent MP4 clips using FFmpeg.",
        "Expose image and video rendering through a FastAPI service and standalone image CLI.",
        "Run the renderer and local n8n environment with Docker Compose.",
    ],
    technologies="Python, Pillow, FastAPI, Uvicorn, FFmpeg, Docker, n8n",
    repository="https://github.com/raimiazeez26/content-forge",
    status="Renderer source and local service are documented; the repository notes that batch n8n workflow exports are not included.",
    notes=[
        "The renderer consumes prepared text; the HTTP API does not itself generate AI content.",
        "Batch generation, Drive upload, and tracking require the separate automation workflows and credentials described by the repository.",
    ],
)
