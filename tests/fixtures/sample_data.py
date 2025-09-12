"""
Sample data for testing
"""
import json
from pathlib import Path

# Sample projects data
SAMPLE_PROJECTS = [
    {
        "name": "Portfolio Website",
        "description": "Personal portfolio built with FastAPI and HTMX",
        "github_url": "https://github.com/user/portfolio",
        "demo_url": "https://portfolio.example.com",
        "technologies": "Python, FastAPI, HTMX, Docker",
        "source": "local"
    },
    {
        "name": "API Service",
        "description": "RESTful API service for data management",
        "github_url": "https://github.com/user/api-service",
        "technologies": "Python, FastAPI, PostgreSQL",
        "source": "local"
    }
]

# Sample GitHub API response
SAMPLE_GITHUB_REPOS = [
    {
        "name": "awesome-project",
        "description": "An awesome open source project",
        "html_url": "https://github.com/user/awesome-project",
        "homepage": "https://awesome-project.com",
        "stargazers_count": 42,
        "language": "Python",
        "updated_at": "2023-12-01T10:00:00Z",
        "fork": False,
        "topics": ["python", "web", "opensource"]
    },
    {
        "name": "cli-tool", 
        "description": "Command line utility",
        "html_url": "https://github.com/user/cli-tool",
        "homepage": None,
        "stargazers_count": 15,
        "language": "Go",
        "updated_at": "2023-11-15T14:30:00Z",
        "fork": False,
        "topics": ["go", "cli", "utility"]
    }
]

# Sample contact submissions
SAMPLE_CONTACTS = [
    {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "message": "Great portfolio! I'd like to discuss a potential collaboration."
    },
    {
        "name": "Bob Smith",
        "email": "bob.smith@company.com", 
        "message": "Interested in your API service. Can we schedule a call?"
    }
]

# Sample resume/locale data
SAMPLE_RESUME_EN = {
    "personal": {
        "name": "Leonardo Murakami",
        "title": "Software Engineer & Site Reliability Engineer",
        "email": "leonardo@example.com",
        "phone": "+55 11 99999-9999",
        "linkedin": "linkedin.com/in/leonardo-murakami",
        "github": "github.com/leonardo-murakami"
    },
    "summary": "Experienced software engineer with expertise in cloud infrastructure, automation, and scalable systems.",
    "company": {
        "name": "Tech Company",
        "description": "Leading technology company focusing on innovative solutions",
        "period": "2020 - Present"
    },
    "roles": [
        {
            "title": "Senior Site Reliability Engineer",
            "period": "2022 - Present",
            "achievements": [
                "Designed and implemented monitoring solutions serving 10M+ daily requests",
                "Reduced system downtime by 50% through proactive alerting and automation",
                "Led incident response for critical production issues"
            ]
        },
        {
            "title": "Software Engineer",
            "period": "2020 - 2022", 
            "achievements": [
                "Developed microservices architecture serving 1M+ users",
                "Implemented CI/CD pipelines reducing deployment time by 70%",
                "Mentored junior developers on best practices"
            ]
        }
    ],
    "education": {
        "degree": "Bachelor of Science in Computer Engineering",
        "institution": "University of São Paulo",
        "description": "Focus on software engineering, algorithms, and distributed systems"
    }
}

SAMPLE_RESUME_PT = {
    "personal": {
        "name": "Leonardo Murakami",
        "title": "Engenheiro de Software & Engenheiro de Confiabilidade",
        "email": "leonardo@example.com",
        "phone": "+55 11 99999-9999",
        "linkedin": "linkedin.com/in/leonardo-murakami",
        "github": "github.com/leonardo-murakami"
    },
    "summary": "Engenheiro de software experiente com expertise em infraestrutura na nuvem, automação e sistemas escaláveis.",
    "company": {
        "name": "Empresa de Tecnologia",
        "description": "Empresa líder em tecnologia focada em soluções inovadoras",
        "period": "2020 - Presente"
    },
    "roles": [
        {
            "title": "Engenheiro de Confiabilidade Sênior",
            "period": "2022 - Presente",
            "achievements": [
                "Projetou e implementou soluções de monitoramento para 10M+ requisições diárias",
                "Reduziu downtime do sistema em 50% através de alertas proativos e automação",
                "Liderou resposta a incidentes para problemas críticos de produção"
            ]
        }
    ],
    "education": {
        "degree": "Bacharelado em Engenharia da Computação",
        "institution": "Universidade de São Paulo",
        "description": "Foco em engenharia de software, algoritmos e sistemas distribuídos"
    }
}


def create_temp_projects_file(temp_dir: Path) -> Path:
    """Create temporary projects.json file for testing"""
    data_dir = temp_dir / "static" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    projects_file = data_dir / "projects.json"
    with projects_file.open("w") as f:
        json.dump(SAMPLE_PROJECTS, f, indent=2)
    
    return projects_file


def create_temp_locale_files(temp_dir: Path) -> tuple[Path, Path]:
    """Create temporary locale files for testing"""
    locales_dir = temp_dir / "static" / "locales"
    locales_dir.mkdir(parents=True, exist_ok=True)
    
    en_file = locales_dir / "en.json"
    pt_file = locales_dir / "pt.json"
    
    with en_file.open("w") as f:
        json.dump(SAMPLE_RESUME_EN, f, indent=2)
    
    with pt_file.open("w") as f:
        json.dump(SAMPLE_RESUME_PT, f, indent=2)
    
    return en_file, pt_file
