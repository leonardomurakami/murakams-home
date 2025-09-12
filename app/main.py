from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import httpx
from typing import Optional

from .config import settings
from .services.github import GitHubService
from .services.email import EmailService
from .services.pdf import PDFService
from .local_data import load_projects, save_contact

app = FastAPI(title="Personal Portfolio", description="Leonardo's Personal Website")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Services
github_service = GitHubService()
email_service = EmailService()
pdf_service = PDFService()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with random GitHub projects"""
    # Get GitHub repositories with error handling
    try:
        github_repos = await github_service.get_repositories(limit=20)  # Get more repos to have variety
        
        # Select 3 random projects (or fewer if less available)
        import random
        random_projects = random.sample(github_repos, min(3, len(github_repos))) if github_repos else []
        
    except Exception as e:
        print(f"Error fetching GitHub repositories for home page: {e}")
        random_projects = []
    
    return templates.TemplateResponse("pages/home.html", {
        "request": request,
        "random_projects": random_projects
    })


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page"""
    return templates.TemplateResponse("pages/about.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, search: Optional[str] = None):
    """Projects page with filtering"""
    # Get GitHub repositories with error handling
    try:
        github_repos = await github_service.get_repositories()
    except Exception:
        # If GitHub service fails, continue with empty list
        github_repos = []

    # Get local projects from JSON
    local_projects = load_projects()

    # Combine and filter projects if search term provided
    all_projects = github_repos + local_projects
    
    if search:
        all_projects = [
            project for project in all_projects 
            if search.lower() in project.get('name', '').lower() or 
               search.lower() in project.get('description', '').lower()
        ]
    
    return templates.TemplateResponse("pages/projects.html", {
        "request": request,
        "projects": all_projects,
        "search": search or ""
    })


@app.get("/contact", response_class=HTMLResponse)
async def contact(request: Request):
    """Contact page"""
    return templates.TemplateResponse("pages/contact.html", {"request": request})


@app.post("/contact")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
):
    """Handle contact form submission"""
    try:
        # Save locally
        save_contact(name, email, message)

        # Send email
        await email_service.send_contact_email(name, email, message)

        # Return success response (HTMX will handle this)
        return templates.TemplateResponse("components/contact_success.html", {"request": request})

    except Exception as e:
        return templates.TemplateResponse("components/contact_error.html", {
            "request": request,
            "error": str(e)
        })


@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    """Resume page"""
    return templates.TemplateResponse("pages/resume.html", {"request": request})


@app.get("/resume/download")
async def download_resume_pdf(language: str = "en"):
    """Download resume as PDF
    
    Args:
        language: Language code ('en' for English, 'pt' for Portuguese)
    """
    try:
        # Generate PDF
        pdf_content = pdf_service.generate_resume_pdf(language)
        
        # Set filename based on language
        filename = f"Leonardo_Murakami_Resume_{'PT' if language == 'pt' else 'EN'}.pdf"
        
        # Return PDF response
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


# HTMX endpoints for dynamic content
@app.get("/htmx/projects/search")
async def htmx_projects_search(request: Request, q: str = ""):
    """HTMX endpoint for project search"""
    # Get GitHub repositories with error handling
    try:
        github_repos = await github_service.get_repositories()
    except Exception:
        # If GitHub service fails, continue with empty list
        github_repos = []

    # Get local projects from JSON
    local_projects = load_projects()

    # Combine and filter projects
    all_projects = github_repos + local_projects
    
    if q:
        all_projects = [
            project for project in all_projects 
            if q.lower() in project.get('name', '').lower() or 
               q.lower() in project.get('description', '').lower()
        ]
    
    return templates.TemplateResponse("components/project_list.html", {
        "request": request,
        "projects": all_projects
    })


@app.post("/htmx/theme/toggle")
async def toggle_theme(request: Request, theme: str = Form(...)):
    """Toggle theme endpoint for HTMX"""
    # This endpoint doesn't need to do much since theme is handled client-side
    # But we return a response to confirm the toggle
    return templates.TemplateResponse("components/theme_toggle.html", {
        "request": request,
        "current_theme": theme
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
