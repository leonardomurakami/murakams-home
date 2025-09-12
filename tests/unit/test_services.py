"""
Tests for application services
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch, mock_open
import httpx
import smtplib
import json
import io

from app.services.github import GitHubService
from app.services.email import EmailService
from app.services.pdf import PDFService


class TestGitHubService:
    """Test GitHub service functionality"""

    def test_init_with_settings(self, mock_settings):
        """Test GitHub service initialization"""
        with patch('app.services.github.settings', mock_settings):
            service = GitHubService()
            
            assert service.base_url == "https://api.github.com"
            assert service.username == mock_settings.github_username
            assert service.token == mock_settings.github_token

    @pytest.mark.asyncio
    async def test_get_repositories_no_username(self):
        """Test get repositories when no username is configured"""
        service = GitHubService()
        service.username = None
        
        result = await service.get_repositories()
        assert result == []

    @pytest.mark.asyncio
    async def test_get_repositories_success(self, mock_github_response):
        """Test successful repository fetching"""
        service = GitHubService()
        service.username = "testuser"
        service.token = "test_token"

        mock_response = Mock()
        mock_response.json.return_value = mock_github_response
        mock_response.raise_for_status.return_value = None

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await service.get_repositories()
            
            assert len(result) == 1
            repo = result[0]
            assert repo["name"] == "test-repo"
            assert repo["description"] == "Test repository"
            assert repo["source"] == "github"
            assert repo["stars"] == 5
            assert "fastapi, python" in repo["technologies"]

    @pytest.mark.asyncio
    async def test_get_repositories_filters_forks(self):
        """Test that forked repositories are filtered out"""
        service = GitHubService()
        service.username = "testuser"

        mock_response_data = [
            {
                "name": "original-repo",
                "description": "Original repository",
                "html_url": "https://github.com/testuser/original-repo",
                "fork": False,
                "stargazers_count": 5,
                "language": "Python",
                "updated_at": "2023-01-01T00:00:00Z",
                "topics": []
            },
            {
                "name": "forked-repo",
                "description": "Forked repository",
                "html_url": "https://github.com/testuser/forked-repo", 
                "fork": True,
                "stargazers_count": 10,
                "language": "Python",
                "updated_at": "2023-01-01T00:00:00Z",
                "topics": []
            }
        ]

        mock_response = Mock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await service.get_repositories()
            
            # Should only return non-forked repo
            assert len(result) == 1
            assert result[0]["name"] == "original-repo"

    @pytest.mark.asyncio
    async def test_get_repositories_http_error(self):
        """Test repository fetching with HTTP error"""
        service = GitHubService()
        service.username = "testuser"

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPError("API Error")

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await service.get_repositories()
            assert result == []

    @pytest.mark.asyncio
    async def test_get_repository_languages_success(self):
        """Test successful repository languages fetching"""
        service = GitHubService()
        service.username = "testuser"
        service.token = "test_token"

        languages_data = {"Python": 2500, "JavaScript": 1200, "HTML": 300}

        mock_response = Mock()
        mock_response.json.return_value = languages_data
        mock_response.raise_for_status.return_value = None

        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            result = await service.get_repository_languages("test-repo")
            
            assert result == languages_data
            # Verify correct API endpoint was called
            mock_client.return_value.__aenter__.return_value.get.assert_called_once()

    @pytest.mark.asyncio 
    async def test_get_repository_languages_no_username(self):
        """Test repository languages fetching with no username"""
        service = GitHubService()
        service.username = None
        
        result = await service.get_repository_languages("test-repo")
        assert result is None

    def test_extract_technologies_with_language_and_topics(self):
        """Test technology extraction from repository data"""
        service = GitHubService()
        
        repo_data = {
            "language": "Python",
            "topics": ["fastapi", "web", "api"]
        }
        
        result = service._extract_technologies(repo_data)
        assert "Python" in result
        assert "fastapi" in result
        assert "web" in result
        assert "api" in result

    def test_extract_technologies_no_language(self):
        """Test technology extraction with no primary language"""
        service = GitHubService()
        
        repo_data = {
            "language": None,
            "topics": ["documentation", "markdown"]
        }
        
        result = service._extract_technologies(repo_data)
        assert "documentation" in result
        assert "markdown" in result


class TestEmailService:
    """Test email service functionality"""

    def test_init_with_settings(self, mock_settings):
        """Test email service initialization"""
        with patch('app.services.email.settings', mock_settings):
            service = EmailService()
            
            assert service.smtp_host == mock_settings.smtp_host
            assert service.smtp_port == mock_settings.smtp_port
            assert service.contact_email == mock_settings.contact_email

    def test_is_mailhog_detection(self):
        """Test MailHog detection"""
        service = EmailService()
        
        # Test MailHog configuration
        service.smtp_host = "mailhog"
        service.smtp_port = 1025
        assert service._is_mailhog() is True
        
        service.smtp_host = "localhost"
        service.smtp_port = 1025
        assert service._is_mailhog() is True
        
        # Test non-MailHog configuration
        service.smtp_host = "smtp.gmail.com"
        service.smtp_port = 587
        assert service._is_mailhog() is False

    @patch('smtplib.SMTP')
    def test_create_smtp_connection_regular(self, mock_smtp):
        """Test SMTP connection creation for regular SMTP servers"""
        service = EmailService()
        service.smtp_host = "smtp.gmail.com"
        service.smtp_port = 587
        service.smtp_username = "user@gmail.com"
        service.smtp_password = "password"
        
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = service._create_smtp_connection()
        
        mock_smtp.assert_called_once_with("smtp.gmail.com", 587)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("user@gmail.com", "password")
        assert result == mock_server

    @patch('smtplib.SMTP')
    def test_create_smtp_connection_mailhog(self, mock_smtp):
        """Test SMTP connection creation for MailHog"""
        service = EmailService()
        service.smtp_host = "mailhog"
        service.smtp_port = 1025
        
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = service._create_smtp_connection()
        
        mock_smtp.assert_called_once_with("mailhog", 1025)
        # Should not call starttls or login for MailHog
        mock_server.starttls.assert_not_called()
        mock_server.login.assert_not_called()
        assert result == mock_server

    @pytest.mark.asyncio
    @patch('smtplib.SMTP')
    async def test_send_contact_email_success(self, mock_smtp, sample_contact_data):
        """Test successful contact email sending"""
        service = EmailService()
        service.smtp_host = "mailhog"
        service.smtp_port = 1025
        service.contact_email = "contact@example.com"
        
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = await service.send_contact_email(
            sample_contact_data["name"],
            sample_contact_data["email"],
            sample_contact_data["message"]
        )
        
        assert result is True
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_contact_email_no_config(self):
        """Test contact email sending with incomplete configuration"""
        service = EmailService()
        service.smtp_host = "smtp.gmail.com"  # Not MailHog
        service.contact_email = None
        
        result = await service.send_contact_email("John", "john@example.com", "Message")
        assert result is False

    @pytest.mark.asyncio
    @patch('smtplib.SMTP')
    async def test_send_contact_email_smtp_error(self, mock_smtp, sample_contact_data):
        """Test contact email sending with SMTP error"""
        service = EmailService()
        service.smtp_host = "mailhog"
        service.smtp_port = 1025
        service.contact_email = "contact@example.com"
        
        mock_server = Mock()
        mock_server.sendmail.side_effect = smtplib.SMTPException("SMTP Error")
        mock_smtp.return_value = mock_server
        
        result = await service.send_contact_email(
            sample_contact_data["name"],
            sample_contact_data["email"],
            sample_contact_data["message"]
        )
        
        assert result is False

    @pytest.mark.asyncio
    @patch('smtplib.SMTP')
    async def test_send_notification_email_success(self, mock_smtp):
        """Test successful notification email sending"""
        service = EmailService()
        service.smtp_host = "mailhog"
        service.smtp_port = 1025
        service.contact_email = "contact@example.com"
        
        mock_server = Mock()
        mock_smtp.return_value = mock_server
        
        result = await service.send_notification_email("Test Subject", "Test Content")
        
        assert result is True
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()


class TestPDFService:
    """Test PDF service functionality"""

    def test_init(self):
        """Test PDF service initialization"""
        service = PDFService()
        assert service.templates_dir.name == "templates"
        assert service.env is not None

    def test_init_custom_templates_dir(self):
        """Test PDF service initialization with custom templates directory"""
        service = PDFService(templates_dir="custom_templates")
        assert service.templates_dir.name == "custom_templates"

    @patch('builtins.open', new_callable=mock_open)
    def test_get_resume_data_english(self, mock_open_func, sample_locales):
        """Test resume data loading for English"""
        service = PDFService()
        
        # Mock file reading - the open call reads the JSON data
        mock_open_func.return_value.__enter__.return_value.read.return_value = json.dumps(sample_locales["en"])
        
        result = service._get_resume_data("en")
        
        assert result["language"] == "en"
        assert "personal_info" in result
        assert "skills" in result
        assert "Programming Languages" in result["skills"]

    @patch('builtins.open')
    def test_get_resume_data_fallback_to_english(self, mock_open_func, sample_locales):
        """Test resume data fallback to English when requested language fails"""
        service = PDFService()
        
        # First call (for requested language) fails, second call (fallback) succeeds  
        def side_effect(*args, **kwargs):
            if 'fr.json' in str(args[0]):
                raise FileNotFoundError("File not found")
            else:
                # Return mock for en.json
                mock_file = mock_open(read_data=json.dumps(sample_locales["en"]))()
                return mock_file
        
        mock_open_func.side_effect = side_effect
        
        result = service._get_resume_data("fr")  # Request French, should fallback to English
        
        assert result["language"] == "en"

    def test_transform_locale_data_english(self, sample_locales):
        """Test locale data transformation for English"""
        service = PDFService()
        
        result = service._transform_locale_data(sample_locales["en"], "en")
        
        assert result["language"] == "en"
        assert result["personal_info"] == sample_locales["en"]["personal"]
        assert "Programming Languages" in result["skills"]
        assert "Python" in result["skills"]["Programming Languages"]

    def test_transform_locale_data_portuguese(self, sample_locales):
        """Test locale data transformation for Portuguese"""
        service = PDFService()
        
        result = service._transform_locale_data(sample_locales["en"], "pt")  # Using EN data but PT language
        
        assert result["language"] == "pt"
        assert "Linguagens de Programação" in result["skills"]
        assert "Python" in result["skills"]["Linguagens de Programação"]

    def test_get_pdf_css(self):
        """Test PDF CSS generation"""
        service = PDFService()
        
        css = service._get_pdf_css()
        
        assert "@page" in css
        assert "size: A4" in css
        assert "font-family" in css
        assert ".header" in css
        assert ".section" in css

    @patch('weasyprint.HTML')
    @patch('weasyprint.CSS')
    @patch.object(PDFService, '_get_resume_data')
    @patch.object(PDFService, '_get_pdf_css')
    def test_generate_resume_pdf_success(self, mock_get_css, mock_get_data, mock_css, mock_html, sample_locales):
        """Test successful PDF generation"""
        service = PDFService()
        
        # Mock data and CSS - _get_resume_data should return transformed data
        transformed_data = service._transform_locale_data(sample_locales["en"], "en")
        mock_get_data.return_value = transformed_data
        mock_get_css.return_value = "body { font-family: Arial; }"
        
        # Mock WeasyPrint objects
        mock_html_instance = Mock()
        mock_css_instance = Mock()
        mock_html.return_value = mock_html_instance
        mock_css.return_value = mock_css_instance
        
        # Mock PDF bytes
        test_pdf_content = b"fake_pdf_content"
        def write_pdf_side_effect(target, stylesheets=None):
            target.write(test_pdf_content)
            
        mock_html_instance.write_pdf.side_effect = write_pdf_side_effect
        
        result = service.generate_resume_pdf("en")
        
        assert result == test_pdf_content
        mock_html.assert_called_once()
        mock_css.assert_called_once()
        mock_html_instance.write_pdf.assert_called_once()

    @patch.object(PDFService, '_get_resume_data')
    def test_generate_resume_pdf_data_error(self, mock_get_data):
        """Test PDF generation with data loading error"""
        service = PDFService()
        mock_get_data.side_effect = Exception("Data loading failed")
        
        with pytest.raises(Exception):
            service.generate_resume_pdf("en")

    @patch('weasyprint.HTML')
    @patch('weasyprint.CSS')  
    @patch.object(PDFService, '_get_resume_data')
    @patch.object(PDFService, '_get_pdf_css')
    def test_generate_resume_pdf_weasyprint_error(self, mock_get_css, mock_get_data, mock_css, mock_html, sample_locales):
        """Test PDF generation with WeasyPrint error"""
        service = PDFService()
        
        # Mock data and CSS - _get_resume_data should return transformed data
        transformed_data = service._transform_locale_data(sample_locales["en"], "en")
        mock_get_data.return_value = transformed_data
        mock_get_css.return_value = "body { font-family: Arial; }"
        
        # Mock WeasyPrint to raise error
        mock_html.side_effect = Exception("WeasyPrint error")
        
        with pytest.raises(Exception):
            service.generate_resume_pdf("en")
