import io
import json
from pathlib import Path
from typing import Optional
import weasyprint
from jinja2 import Environment, FileSystemLoader


class PDFService:
    """Service for generating PDF documents"""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.env = Environment(loader=FileSystemLoader(self.templates_dir))
    
    def generate_resume_pdf(self, language: str = "en") -> bytes:
        """Generate PDF resume from HTML template
        
        Args:
            language: Language code ('en' or 'pt')
            
        Returns:
            PDF content as bytes
        """
        # Get the appropriate template data based on language
        template_data = self._get_resume_data(language)
        
        # Render the PDF template
        template = self.env.get_template("pdf/resume_pdf.html")
        html_content = template.render(**template_data)
        
        # Create CSS for PDF
        css_content = self._get_pdf_css()
        
        # Generate PDF
        html_doc = weasyprint.HTML(string=html_content)
        css_doc = weasyprint.CSS(string=css_content)
        
        pdf_bytes = io.BytesIO()
        html_doc.write_pdf(pdf_bytes, stylesheets=[css_doc])
        pdf_bytes.seek(0)
        
        return pdf_bytes.getvalue()
    
    def _get_resume_data(self, language: str) -> dict:
        """Get resume data based on language"""
        
        # Load locale data from JSON files
        locale_file = Path("static/locales") / f"{language}.json"
        
        try:
            with open(locale_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Transform the data structure for the PDF template
            return self._transform_locale_data(data, language)
        except FileNotFoundError:
            # Fallback to English if file not found
            if language != "en":
                return self._get_resume_data("en")
            raise
        except Exception as e:
            # Fallback to English for any other error
            if language != "en":
                return self._get_resume_data("en")
            raise
    
    def _transform_locale_data(self, data: dict, language: str) -> dict:
        """Transform locale data to PDF template format"""
        return {
            "language": language,
            "personal_info": data["personal"],
            "summary": data["summary"],
            "company": data["company"],
            "experiences": data["roles"],
            "skills": {
                "Programming Languages": ["Python", "Go", "C/C++", "Bash", "SQL"],
                "Cloud & Infrastructure": ["AWS", "Kubernetes", "Docker", "Terraform", "Helm"],
                "Monitoring & Observability": ["Prometheus", "Grafana", "CloudWatch", "Datadog", "ELK Stack"],
                "Data & ML": ["MLOps", "Data Pipelines", "PostgreSQL", "BigQuery", "Scikit-learn"],
                "Tools & Methodologies": ["Git", "Linux", "CI/CD", "SLI/SLO", "Incident Response"]
            } if language == "en" else {
                "Linguagens de Programação": ["Python", "Go", "C/C++", "Bash", "SQL"],
                "Nuvem e Infraestrutura": ["AWS", "Kubernetes", "Docker", "Terraform", "Helm"],
                "Monitoramento e Observabilidade": ["Prometheus", "Grafana", "CloudWatch", "Datadog", "ELK Stack"],
                "Dados e ML": ["MLOps", "Pipelines de Dados", "PostgreSQL", "BigQuery", "Scikit-learn"],
                "Ferramentas e Metodologias": ["Git", "Linux", "CI/CD", "SLI/SLO", "Resposta a Incidentes"]
            },
            "education": data["education"]
        }
    
    def _get_pdf_css(self) -> str:
        """CSS optimized for PDF generation"""
        return """
        @page {
            size: A4;
            margin: 1cm;
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'DejaVu Sans', Arial, sans-serif;
            font-size: 11px;
            line-height: 1.4;
            color: #333;
            margin: 0;
            padding: 0;
        }
        
        .header {
            background: linear-gradient(135deg, #3b82f6, #1e40af);
            color: white;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 24px;
            margin: 0 0 5px 0;
            font-weight: bold;
        }
        
        .header .title {
            font-size: 16px;
            margin: 0 0 15px 0;
            opacity: 0.9;
        }
        
        .header .contact {
            display: flex;
            justify-content: center;
            gap: 20px;
            font-size: 10px;
            flex-wrap: wrap;
        }
        
        .section {
            margin-bottom: 20px;
            page-break-inside: avoid;
        }
        
        .section-title {
            font-size: 14px;
            font-weight: bold;
            color: #1e40af;
            margin-bottom: 10px;
            padding-bottom: 3px;
            border-bottom: 2px solid #3b82f6;
        }
        
        .summary {
            font-size: 11px;
            line-height: 1.5;
            text-align: justify;
        }
        
        .company-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding: 10px;
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
        }
        
        .company-icon {
            width: 30px;
            height: 30px;
            background-color: #3b82f6;
            color: white;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 15px;
            font-weight: bold;
        }
        
        .company-info h3 {
            font-size: 16px;
            margin: 0 0 3px 0;
            color: #1e40af;
        }
        
        .company-info .period {
            font-size: 10px;
            color: #666;
            margin: 0 0 2px 0;
        }
        
        .company-info .description {
            font-size: 9px;
            color: #999;
            margin: 0;
        }
        
        .experience {
            margin-bottom: 15px;
            padding: 12px;
            background-color: #fff;
            border: 1px solid #e5e7eb;
            border-radius: 6px;
        }
        
        .experience-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .experience-title {
            font-size: 12px;
            font-weight: bold;
            color: #1f2937;
        }
        
        .experience-period {
            font-size: 9px;
            color: #6b7280;
            background-color: #f3f4f6;
            padding: 2px 8px;
            border-radius: 12px;
        }
        
        .achievements {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .achievements li {
            margin-bottom: 6px;
            padding-left: 15px;
            position: relative;
            font-size: 10px;
            line-height: 1.4;
        }
        
        .achievements li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #3b82f6;
            font-weight: bold;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
        }
        
        .skill-category {
            margin-bottom: 12px;
        }
        
        .skill-category h4 {
            font-size: 11px;
            font-weight: bold;
            color: #1f2937;
            margin: 0 0 6px 0;
        }
        
        .skill-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }
        
        .skill-tag {
            background-color: #e0e7ff;
            color: #3730a3;
            padding: 2px 6px;
            border-radius: 12px;
            font-size: 9px;
            font-weight: 500;
        }
        
        .education {
            padding: 12px;
            background-color: #f8fafc;
            border-left: 4px solid #3b82f6;
        }
        
        .education h4 {
            font-size: 12px;
            font-weight: bold;
            color: #1f2937;
            margin: 0 0 3px 0;
        }
        
        .education .institution {
            font-size: 11px;
            color: #3b82f6;
            font-weight: 600;
            margin: 0 0 6px 0;
        }
        
        .education .description {
            font-size: 10px;
            color: #6b7280;
            line-height: 1.4;
        }
        """