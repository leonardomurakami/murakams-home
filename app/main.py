from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import httpx
from typing import Optional

from .database import get_db, engine
from .models import Base, Project, Contact
from .config import settings
from .services.github import GitHubService
from .services.email import EmailService
from .services.pdf import PDFService

# Create database tables
Base.metadata.create_all(bind=engine)

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
    """Home page"""
    return templates.TemplateResponse("pages/home.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page"""
    return templates.TemplateResponse("pages/about.html", {"request": request})


@app.get("/projects", response_class=HTMLResponse)
async def projects(request: Request, search: Optional[str] = None, db: Session = Depends(get_db)):
    """Projects page with filtering"""
    # Get GitHub repositories
    github_repos = await github_service.get_repositories()
    
    # Get local projects from database
    local_projects = db.query(Project).all()
    
    # Combine and filter projects if search term provided
    all_projects = github_repos + [project.__dict__ for project in local_projects]
    
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
    db: Session = Depends(get_db)
):
    """Handle contact form submission"""
    try:
        # Save to database
        contact_entry = Contact(name=name, email=email, message=message)
        db.add(contact_entry)
        db.commit()
        
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
async def htmx_projects_search(request: Request, q: str = "", db: Session = Depends(get_db)):
    """HTMX endpoint for project search"""
    # Get GitHub repositories
    github_repos = await github_service.get_repositories()
    
    # Get local projects from database
    local_projects = db.query(Project).all()
    
    # Combine and filter projects
    all_projects = github_repos + [project.__dict__ for project in local_projects]
    
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
