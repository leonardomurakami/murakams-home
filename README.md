# Personal Portfolio Website

A modern, responsive personal portfolio website built with **FastAPI** and **HTMX**, featuring a clean design with Tailwind CSS and dynamic functionality.

## 🚀 Features

- **Modern Tech Stack**: FastAPI + HTMX + Tailwind CSS
- **Adaptive Sky Design**: Dark mode features a cosmic night sky with stars, shooting stars, and cosmic portal; Light mode shows a beautiful morning sky with smooth cartoonish clouds, flying birds, and a radiant sun
- **Responsive Design**: Mobile-first approach with dark/light theme toggle
- **Dynamic Content**: Real-time search and filtering with HTMX
- **GitHub Integration**: Automatically displays your GitHub repositories
- **Contact Form**: Functional contact form with email notifications
- **Docker Ready**: Full containerization with docker-compose
- **Modular Structure**: Easy to extend with new pages and features

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Jinja2** - Template engine for server-side rendering
- **HTTPX** - Async HTTP client for GitHub API integration
- **Pydantic** - Data validation using Python type annotations

### Frontend
- **HTMX** - High power tools for HTML
- **Tailwind CSS** - Utility-first CSS framework
- **Font Awesome** - Icons and visual elements
- **Vanilla JavaScript** - For theme switching and interactions

### Infrastructure
- **Docker** - Containerization
- **Redis** - Caching (optional)
- **Nginx** - Reverse proxy and static file serving

### Dependency Management
- **uv** - Extremely fast Python package manager (10-100x faster than pip)
- **Lock file** - Reproducible installations with uv.lock
- **Standard pyproject.toml** - Modern Python packaging standards

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)
- uv (for fast dependency management)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd murakams-home
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start the development environment**
   ```bash
   # Development
   docker-compose -f docker-compose.dev.yml up --build

   # Production
   docker-compose up --build
   ```

4. **Access the application**
   - Website: http://localhost:8000
   - MailHog Email Testing (dev mode): http://localhost:8025

### Local Development

1. **Install dependencies**
   ```bash
   # Install uv if you haven't already
   pip install uv
   
   # Install dependencies (much faster than pip!)
   uv pip install -r requirements.txt
   
   # For development with dev dependencies
   uv pip install -r requirements-dev.txt
   ```

2. **Set up environment**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```env
# GitHub Integration
GITHUB_USERNAME=your-github-username
GITHUB_TOKEN=your-github-token  # Optional, for higher rate limits

# Email Configuration (for contact form)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
CONTACT_EMAIL=your-contact@email.com

# App Configuration
SECRET_KEY=your-secret-key-here
DEBUG=true
```

### GitHub Integration

To display your GitHub repositories:
1. Set `GITHUB_USERNAME` in your `.env` file
2. Optionally set `GITHUB_TOKEN` for higher API rate limits

### Email Configuration

For the contact form to work:
1. Set up SMTP credentials in your `.env` file
2. For Gmail, use an "App Password" instead of your regular password

#### Local Email Testing with MailHog

For development and testing, both Docker Compose configurations include MailHog, a local SMTP server that captures emails without sending them:

**Development Mode (docker-compose.dev.yml):**
```bash
# Start with MailHog automatically included
docker-compose -f docker-compose.dev.yml up --build

# Access MailHog web interface
# http://localhost:8025
```

**Production Mode (docker-compose.yml):**
```bash
# Start with dev profile to include MailHog
docker-compose --profile dev up --build

# Access MailHog web interface
# http://localhost:8025
```

**Features:**
- **SMTP Server**: Listens on port 1025
- **Web Interface**: View captured emails at http://localhost:8025
- **No Real Emails**: All emails are captured locally, perfect for testing
- **Automatic Configuration**: Development environment automatically uses MailHog

When using the development Docker Compose, the email service will automatically use MailHog instead of external SMTP servers.

## 📁 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   └── services/
│       ├── github.py        # GitHub API integration
│       └── email.py         # Email service
├── templates/
│   ├── base.html            # Base template
│   ├── pages/               # Page templates
│   └── components/          # Reusable components
├── static/
│   └── css/
│       └── custom.css       # Custom styles
├── docker-compose.yml       # Production compose
├── docker-compose.dev.yml   # Development compose
├── Dockerfile
├── pyproject.toml           # Project metadata and dependencies
└── requirements.txt         # Pip dependencies
```

## 🎨 Customization

### Adding New Pages

1. Create a new template in `templates/pages/`
2. Add a route in `app/main.py`
3. Update navigation in `templates/base.html`

### Styling

- **Dynamic Themes**: Dark mode creates an immersive space atmosphere with cosmic portal; Light mode provides a serene morning sky experience with a beautiful animated sun
- **Interactive Elements**: Mouse movement creates sparkles, shooting stars appear randomly
- **Accessibility**: Respects `prefers-reduced-motion` for users who need it
- Modify `static/css/custom.css` for custom styles
- Use Tailwind classes in templates
- Theme colors can be customized in the Tailwind config

### Branding

- **Logo Files Available**:
  - `logo.svg` - Full logo with dark blue background
  - `logo_no_background.svg` - Logo without background (used in circular containers)
  - `logo.png` - PNG version for compatibility and social media
- **Usage**: Different logo versions used contextually throughout the site
- **Favicon**: Automatically generated from your logo
- **Colors**: Logo colors are integrated with the site theme
- **PWA**: Web app manifest configured for mobile installation

### Content

- Update personal information in templates
- Add your projects to the JSON file or via GitHub integration
- Customize the about page content
- Update social media links in the footer
- Replace logo files in `static/img/` with your own

## 🔧 Development

### Running Tests
```bash
# Install dev dependencies first
uv pip install -r requirements-dev.txt

# Run tests
pytest
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy app/
```

## 🚀 Deployment

### Docker Deployment

1. **Build and run with docker-compose**
   ```bash
   docker-compose up -d
   ```

2. **Set up Nginx** (configuration included)

3. **Configure SSL** (recommended for production)

### Manual Deployment

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**

3. **Run with Gunicorn**
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

## 📝 Features to Add

- [ ] Blog functionality
- [ ] Project categories and tags
- [ ] Admin panel for content management
- [ ] Analytics integration
- [ ] SEO optimization
- [ ] Performance monitoring
- [ ] Automated backups
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- HTMX for making frontend interactivity simple
- Tailwind CSS for the utility-first approach
- The open-source community for inspiration and tools

---

**Built with ❤️ by Leonardo Murakami**
