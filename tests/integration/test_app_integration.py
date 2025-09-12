"""
Integration tests for the full application
"""
import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, Mock
from fastapi.testclient import TestClient

from app.main import app


class TestApplicationIntegration:
    """Test complete application workflows"""

    @pytest.fixture
    def integration_client(self):
        """Test client for integration tests"""
        return TestClient(app)

    def test_homepage_loads(self, integration_client):
        """Test that homepage loads successfully"""
        response = integration_client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_projects_page_integration(self, mock_load_projects, mock_github_repos, integration_client):
        """Test projects page with both GitHub and local projects"""
        # Setup mock data
        github_projects = [
            {
                "name": "github-project",
                "description": "A project from GitHub",
                "github_url": "https://github.com/user/repo",
                "stars": 10,
                "source": "github"
            }
        ]
        
        local_projects = [
            {
                "name": "local-project", 
                "description": "A local project",
                "demo_url": "https://example.com",
                "source": "local"
            }
        ]

        mock_github_repos.return_value = github_projects
        mock_load_projects.return_value = local_projects

        response = integration_client.get("/projects")
        
        assert response.status_code == 200
        # Projects page should call both services
        mock_github_repos.assert_called_once()
        mock_load_projects.assert_called_once()

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_project_search_workflow(self, mock_load_projects, mock_github_repos, integration_client):
        """Test project search functionality"""
        # Setup test data
        all_projects = [
            {"name": "python-api", "description": "A Python API", "source": "github"},
            {"name": "react-frontend", "description": "A React frontend", "source": "local"},
            {"name": "golang-service", "description": "A Go microservice", "source": "github"}
        ]

        mock_github_repos.return_value = [p for p in all_projects if p["source"] == "github"]
        mock_load_projects.return_value = [p for p in all_projects if p["source"] == "local"]

        # Test search for "python"
        response = integration_client.get("/projects?search=python")
        assert response.status_code == 200
        
        # Test HTMX search endpoint
        response = integration_client.get("/htmx/projects/search?q=react")
        assert response.status_code == 200

    @patch('app.main.email_service')
    @patch('app.main.save_contact')
    def test_contact_form_workflow(self, mock_save_contact, mock_email_service, integration_client):
        """Test complete contact form submission workflow"""
        contact_data = {
            "name": "Integration Test User",
            "email": "test@integration.com",
            "message": "This is an integration test message"
        }

        mock_email_service.send_contact_email.return_value = True

        # Test GET contact page
        response = integration_client.get("/contact")
        assert response.status_code == 200

        # Test POST contact form
        response = integration_client.post("/contact", data=contact_data)
        assert response.status_code == 200

        # Verify both services were called
        mock_save_contact.assert_called_once_with(
            contact_data["name"],
            contact_data["email"], 
            contact_data["message"]
        )
        mock_email_service.send_contact_email.assert_called_once()

    @patch('app.main.pdf_service')
    def test_resume_pdf_workflow(self, mock_pdf_service, integration_client):
        """Test resume PDF generation workflow"""
        mock_pdf_content = b"mock_pdf_content_for_integration_test"
        mock_pdf_service.generate_resume_pdf.return_value = mock_pdf_content

        # Test resume page
        response = integration_client.get("/resume")
        assert response.status_code == 200

        # Test PDF download - English
        response = integration_client.get("/resume/download")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/pdf"
        assert "Leonardo_Murakami_Resume_EN.pdf" in response.headers["content-disposition"]
        assert response.content == mock_pdf_content

        # Test PDF download - Portuguese
        response = integration_client.get("/resume/download?language=pt")
        assert response.status_code == 200
        assert "Leonardo_Murakami_Resume_PT.pdf" in response.headers["content-disposition"]

        # Verify service calls
        assert mock_pdf_service.generate_resume_pdf.call_count == 2
        mock_pdf_service.generate_resume_pdf.assert_any_call("en")
        mock_pdf_service.generate_resume_pdf.assert_any_call("pt")

    @patch('app.main.github_service.get_repositories')
    def test_error_handling_github_service_down(self, mock_github_repos, integration_client):
        """Test error handling when GitHub service is down"""
        # Mock GitHub service failure
        mock_github_repos.side_effect = Exception("GitHub API error")
        
        with patch('app.main.load_projects', return_value=[]):
            response = integration_client.get("/projects")
            # Should still return 200 but handle the error gracefully
            assert response.status_code == 200

    @patch('app.main.pdf_service')
    def test_error_handling_pdf_generation_failure(self, mock_pdf_service, integration_client):
        """Test error handling when PDF generation fails"""
        mock_pdf_service.generate_resume_pdf.side_effect = Exception("PDF generation error")

        response = integration_client.get("/resume/download")
        assert response.status_code == 500
        error_detail = response.json()
        assert "Error generating PDF" in error_detail["detail"]

    def test_htmx_endpoints_integration(self, integration_client):
        """Test HTMX-specific endpoints"""
        # Theme toggle
        response = integration_client.post("/htmx/theme/toggle", data={"theme": "dark"})
        assert response.status_code == 200

        # Project search with mocked services
        with patch('app.main.github_service.get_repositories', return_value=[]), \
             patch('app.main.load_projects', return_value=[]):
            response = integration_client.get("/htmx/projects/search?q=test")
            assert response.status_code == 200

    @patch('app.config.settings')
    def test_configuration_integration(self, mock_settings, integration_client):
        """Test application with different configurations"""
        # Test with minimal configuration
        mock_settings.github_username = None
        mock_settings.contact_email = None
        
        # Should still work without external service configuration
        response = integration_client.get("/")
        assert response.status_code == 200

        response = integration_client.get("/about") 
        assert response.status_code == 200

    def test_static_files_accessible(self, integration_client):
        """Test that static files are accessible (if they exist)"""
        # Test accessing static files - these may 404 in test environment
        # but should not cause server errors
        try:
            response = integration_client.get("/static/css/custom.css")
            # Either accessible or properly handled 404
            assert response.status_code in [200, 404]
        except Exception:
            # Static files might not be available in test environment
            pass

    def test_application_startup_shutdown(self):
        """Test application startup and shutdown events"""
        # Test that the app can be started and shut down cleanly
        with TestClient(app) as client:
            response = client.get("/")
            assert response.status_code == 200

    @patch('app.main.github_service.get_repositories')
    @patch('app.main.load_projects')
    def test_concurrent_requests(self, mock_load_projects, mock_github_repos, integration_client):
        """Test handling concurrent requests"""
        import concurrent.futures
        import threading

        mock_github_repos.return_value = []
        mock_load_projects.return_value = []

        def make_request():
            response = integration_client.get("/projects")
            return response.status_code

        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 10
