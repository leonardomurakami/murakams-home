"""
Tests for the main FastAPI application
"""
import pytest
from unittest.mock import patch, Mock, AsyncMock
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app


class TestMainEndpoints:
    """Test main application endpoints"""

    def test_home_endpoint(self, client: TestClient):
        """Test home page endpoint"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    def test_about_endpoint(self, client: TestClient):
        """Test about page endpoint"""
        response = client.get("/about")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    def test_contact_get_endpoint(self, client: TestClient):
        """Test contact page GET endpoint"""
        response = client.get("/contact")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    def test_resume_endpoint(self, client: TestClient):
        """Test resume page endpoint"""
        response = client.get("/resume")
        assert response.status_code == status.HTTP_200_OK
        assert "text/html" in response.headers["content-type"]

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_projects_endpoint_no_search(self, mock_load_projects, mock_github_repos, client: TestClient):
        """Test projects page without search"""
        # Mock data
        mock_github_repos.return_value = [
            {
                "name": "github-repo",
                "description": "A GitHub repository",
                "github_url": "https://github.com/user/repo",
                "source": "github"
            }
        ]
        mock_load_projects.return_value = [
            {
                "name": "local-project",
                "description": "A local project", 
                "source": "local"
            }
        ]

        response = client.get("/projects")
        assert response.status_code == status.HTTP_200_OK
        mock_github_repos.assert_called_once()
        mock_load_projects.assert_called_once()

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_projects_endpoint_with_search(self, mock_load_projects, mock_github_repos, client: TestClient):
        """Test projects page with search query"""
        # Mock data
        mock_github_repos.return_value = [
            {
                "name": "python-api",
                "description": "A Python API",
                "source": "github"
            }
        ]
        mock_load_projects.return_value = [
            {
                "name": "javascript-frontend",
                "description": "A JavaScript frontend",
                "source": "local"
            }
        ]

        response = client.get("/projects?search=python")
        assert response.status_code == status.HTTP_200_OK
        mock_github_repos.assert_called_once()
        mock_load_projects.assert_called_once()

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_htmx_projects_search(self, mock_load_projects, mock_github_repos, client: TestClient):
        """Test HTMX project search endpoint"""
        # Mock data
        mock_github_repos.return_value = [
            {
                "name": "test-repo",
                "description": "Test repository",
                "source": "github"
            }
        ]
        mock_load_projects.return_value = []

        response = client.get("/htmx/projects/search?q=test")
        assert response.status_code == status.HTTP_200_OK
        mock_github_repos.assert_called_once()
        mock_load_projects.assert_called_once()

    @patch('app.main.email_service.send_contact_email')
    @patch('app.main.save_contact')
    def test_contact_submit_success(self, mock_save_contact, mock_send_email, client: TestClient, sample_contact_data):
        """Test successful contact form submission"""
        mock_send_email.return_value = True

        response = client.post("/contact", data=sample_contact_data)
        assert response.status_code == status.HTTP_200_OK
        
        mock_save_contact.assert_called_once_with(
            sample_contact_data["name"],
            sample_contact_data["email"], 
            sample_contact_data["message"]
        )
        mock_send_email.assert_called_once_with(
            sample_contact_data["name"],
            sample_contact_data["email"],
            sample_contact_data["message"]
        )

    @patch('app.main.email_service.send_contact_email')
    @patch('app.main.save_contact')
    def test_contact_submit_email_failure(self, mock_save_contact, mock_send_email, client: TestClient, sample_contact_data):
        """Test contact form submission with email service failure"""
        mock_send_email.side_effect = Exception("Email service error")

        response = client.post("/contact", data=sample_contact_data)
        assert response.status_code == status.HTTP_200_OK  # Should still return 200 but show error template
        
        mock_save_contact.assert_called_once()
        mock_send_email.assert_called_once()

    def test_contact_submit_missing_fields(self, client: TestClient):
        """Test contact form submission with missing required fields"""
        response = client.post("/contact", data={"name": "John"})  # Missing email and message
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @patch('app.main.pdf_service.generate_resume_pdf')
    def test_download_resume_pdf_default_language(self, mock_generate_pdf, client: TestClient):
        """Test PDF resume download with default language (English)"""
        mock_generate_pdf.return_value = b"fake_pdf_content"

        response = client.get("/resume/download")
        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/pdf"
        assert "Leonardo_Murakami_Resume_EN.pdf" in response.headers["content-disposition"]
        mock_generate_pdf.assert_called_once_with("en")

    @patch('app.main.pdf_service.generate_resume_pdf')
    def test_download_resume_pdf_portuguese(self, mock_generate_pdf, client: TestClient):
        """Test PDF resume download in Portuguese"""
        mock_generate_pdf.return_value = b"fake_pdf_content"

        response = client.get("/resume/download?language=pt")
        assert response.status_code == status.HTTP_200_OK
        assert "Leonardo_Murakami_Resume_PT.pdf" in response.headers["content-disposition"]
        mock_generate_pdf.assert_called_once_with("pt")

    @patch('app.main.pdf_service.generate_resume_pdf')
    def test_download_resume_pdf_error(self, mock_generate_pdf, client: TestClient):
        """Test PDF resume download with generation error"""
        mock_generate_pdf.side_effect = Exception("PDF generation failed")

        response = client.get("/resume/download")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Error generating PDF" in response.json()["detail"]

    def test_htmx_theme_toggle(self, client: TestClient):
        """Test HTMX theme toggle endpoint"""
        response = client.post("/htmx/theme/toggle", data={"theme": "dark"})
        assert response.status_code == status.HTTP_200_OK
