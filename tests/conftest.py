"""
Shared pytest fixtures and configuration
"""
import os
import tempfile
import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from pathlib import Path
import json

from app.main import app
from app.config import Settings


@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_settings():
    """Mock settings for testing"""
    return Settings(
        github_username="testuser",
        github_token="test_token",
        smtp_host="localhost",
        smtp_port=1025,
        smtp_username=None,
        smtp_password=None,
        contact_email="test@example.com",
        secret_key="test-secret-key",
        debug=True
    )


@pytest.fixture
def temp_data_dir():
    """Temporary directory for test data files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create test data structure
        data_dir = Path(temp_dir) / "static" / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        # Create test projects.json
        projects_data = [
            {
                "name": "Test Project",
                "description": "A test project",
                "github_url": "https://github.com/test/project",
                "demo_url": "https://test-project.com",
                "technologies": "Python, FastAPI",
                "source": "local"
            }
        ]
        
        projects_file = data_dir / "projects.json"
        with projects_file.open("w") as f:
            json.dump(projects_data, f)
        
        yield temp_dir


@pytest.fixture
def mock_github_response():
    """Mock GitHub API response"""
    return [
        {
            "name": "test-repo",
            "description": "Test repository",
            "html_url": "https://github.com/testuser/test-repo",
            "homepage": "https://test-repo.com",
            "stargazers_count": 5,
            "language": "Python",
            "updated_at": "2023-01-01T00:00:00Z",
            "fork": False,
            "topics": ["fastapi", "python"]
        }
    ]


@pytest.fixture
def mock_httpx_client():
    """Mock httpx.AsyncClient"""
    with patch("httpx.AsyncClient") as mock_client:
        yield mock_client


@pytest.fixture
def mock_smtp_server():
    """Mock SMTP server"""
    with patch("smtplib.SMTP") as mock_smtp:
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        yield mock_server


@pytest.fixture
def mock_weasyprint():
    """Mock WeasyPrint for PDF generation"""
    with patch("weasyprint.HTML") as mock_html, \
         patch("weasyprint.CSS") as mock_css:
        mock_html_instance = Mock()
        mock_css_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_css.return_value = mock_css_instance
        
        # Mock PDF bytes
        mock_html_instance.write_pdf.return_value = None
        
        yield {
            "html": mock_html,
            "css": mock_css,
            "html_instance": mock_html_instance,
            "css_instance": mock_css_instance
        }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables and paths"""
    # Set test environment
    os.environ["TESTING"] = "1"
    
    # Ensure we don't accidentally use real files
    original_cwd = os.getcwd()
    
    yield
    
    # Cleanup
    os.chdir(original_cwd)
    if "TESTING" in os.environ:
        del os.environ["TESTING"]


@pytest.fixture
def sample_contact_data():
    """Sample contact form data"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "message": "This is a test message"
    }


@pytest.fixture
def sample_locales():
    """Sample locale data for PDF generation"""
    return {
        "en": {
            "personal": {
                "name": "John Doe",
                "title": "Software Engineer",
                "email": "john@example.com",
                "phone": "+1234567890"
            },
            "summary": "Experienced software engineer...",
            "company": {
                "name": "Test Company",
                "description": "A test company",
                "period": "2020 - Present"
            },
            "roles": [
                {
                    "title": "Senior Engineer",
                    "period": "2021 - Present",
                    "achievements": ["Built great things", "Led team"]
                }
            ],
            "education": {
                "degree": "Computer Science",
                "institution": "Test University",
                "description": "Studied computer science"
            }
        }
    }
