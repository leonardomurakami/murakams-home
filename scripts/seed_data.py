#!/usr/bin/env python3
"""
Sample data seeding script for the portfolio website.
Run this script to populate the database with sample data for development and testing.
"""

import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base, Project, Skill, Experience
from app.database import engine


def create_sample_projects():
    """Create sample project data"""
    projects = [
        Project(
            name="E-Commerce Platform",
            description="A full-stack e-commerce solution built with FastAPI and React. Features include user authentication, product catalog, shopping cart, payment processing, and admin dashboard.",
            technologies="Python, FastAPI, React, PostgreSQL, Docker, Stripe",
            github_url="https://github.com/yourusername/ecommerce-platform",
            demo_url="https://ecommerce-demo.example.com",
            featured=True
        ),
        Project(
            name="Task Management API",
            description="RESTful API for task management with user authentication, team collaboration, and real-time updates using WebSockets.",
            technologies="Python, FastAPI, SQLAlchemy, WebSockets, Redis",
            github_url="https://github.com/yourusername/task-management-api",
            featured=True
        ),
        Project(
            name="Data Analytics Dashboard",
            description="Interactive dashboard for data visualization and analytics using modern web technologies and chart libraries.",
            technologies="JavaScript, React, D3.js, Node.js, MongoDB",
            github_url="https://github.com/yourusername/analytics-dashboard",
            demo_url="https://analytics-demo.example.com",
            featured=False
        ),
        Project(
            name="Personal Finance Tracker",
            description="Mobile-friendly web application for tracking personal expenses, income, and financial goals with beautiful visualizations.",
            technologies="Python, Flask, Chart.js, SQLite, Bootstrap",
            github_url="https://github.com/yourusername/finance-tracker",
            featured=False
        ),
        Project(
            name="Weather Forecast App",
            description="Real-time weather application with location-based forecasts, weather maps, and historical data analysis.",
            technologies="JavaScript, React, OpenWeather API, Tailwind CSS",
            github_url="https://github.com/yourusername/weather-app",
            demo_url="https://weather-demo.example.com",
            featured=False
        )
    ]
    return projects


def create_sample_skills():
    """Create sample skill data"""
    skills = [
        # Programming Languages
        Skill(name="Python", category="programming", proficiency=5, icon_name="fab fa-python"),
        Skill(name="Go", category="programming", proficiency=4, icon_name="fab fa-golang"),
        Skill(name="C", category="programming", proficiency=4, icon_name="fas fa-code"),
        Skill(name="C++", category="programming", proficiency=4, icon_name="fas fa-code"),
        Skill(name="Bash", category="programming", proficiency=3, icon_name="fas fa-terminal"),
        
        # Cloud & Infrastructure
        Skill(name="AWS", category="cloud", proficiency=5, icon_name="fab fa-aws"),
        Skill(name="Kubernetes", category="cloud", proficiency=5, icon_name="fas fa-dharmachakra"),
        Skill(name="Docker", category="cloud", proficiency=5, icon_name="fab fa-docker"),
        Skill(name="Terraform", category="cloud", proficiency=5, icon_name="fas fa-cube"),
        Skill(name="Helm", category="cloud", proficiency=5, icon_name="fas fa-anchor"),
        
        # Monitoring & Observability
        Skill(name="Prometheus", category="monitoring", proficiency=4, icon_name="fas fa-chart-line"),
        Skill(name="Grafana", category="monitoring", proficiency=4, icon_name="fas fa-chart-bar"),
        Skill(name="CloudWatch", category="monitoring", proficiency=4, icon_name="fab fa-aws"),
        Skill(name="Datadog", category="monitoring", proficiency=4, icon_name="fas fa-dog"),
        Skill(name="ELK Stack", category="monitoring", proficiency=3, icon_name="fas fa-search"),
        
        # Frameworks (limited experience)
        Skill(name="React", category="frameworks", proficiency=3, icon_name="fab fa-react"),
        
        # Data & ML
        Skill(name="MLOps", category="data", proficiency=4, icon_name="fas fa-robot"),
        Skill(name="Data Pipelines", category="data", proficiency=4, icon_name="fas fa-stream"),
        Skill(name="PostgreSQL", category="data", proficiency=4, icon_name="fas fa-database"),
        Skill(name="BigQuery", category="data", proficiency=3, icon_name="fas fa-database"),
        
        # Methodologies
        Skill(name="SRE Practices", category="methodologies", proficiency=5, icon_name="fas fa-server"),
        Skill(name="Incident Response", category="methodologies", proficiency=5, icon_name="fas fa-exclamation-triangle"),
        Skill(name="CI/CD", category="methodologies", proficiency=4, icon_name="fas fa-sync"),
        Skill(name="Infrastructure as Code", category="methodologies", proficiency=5, icon_name="fas fa-code"),
    ]
    return skills


def create_sample_experiences():
    """Create sample experience data"""
    experiences = [
        Experience(
            company="Loft",
            position="Site Reliability Engineer L2",
            description="Leading incident response and post-mortem processes to maintain high system availability. Designing and implementing monitoring, alerting, and observability solutions. Mentoring junior SREs and establishing reliability best practices across teams.",
            start_date="Jan 2025",
            end_date="Present",
            location="Remote",
            company_url="https://loft.com.br"
        ),
        Experience(
            company="Loft",
            position="Junior Site Reliability Engineer",
            description="Managed Kubernetes clusters and automated infrastructure deployments using Terraform. Implemented monitoring and alerting systems to proactively identify system issues. Participated in on-call rotations and incident response procedures.",
            start_date="Jan 2024",
            end_date="Dec 2024",
            location="Remote",
            company_url="https://loft.com.br"
        ),
        Experience(
            company="Loft",
            position="Junior MLOps Engineer",
            description="Built and maintained ML model deployment pipelines using Docker and Kubernetes. Developed infrastructure automation for ML training and inference workloads. Collaborated with data science teams to productionize machine learning models.",
            start_date="Jan 2022",
            end_date="Dec 2023",
            location="Remote",
            company_url="https://loft.com.br"
        ),
        Experience(
            company="Loft",
            position="Junior Data Scientist",
            description="Developed machine learning models for real estate price prediction and market analysis. Created data pipelines and ETL processes using Python and SQL. Collaborated with product teams to deliver data-driven insights and recommendations.",
            start_date="Jan 2020",
            end_date="Dec 2021",
            location="Remote",
            company_url="https://loft.com.br"
        ),
        Experience(
            company="Loft",
            position="Data Scientist Intern",
            description="Started journey in tech by learning data science fundamentals and machine learning. Worked on data analysis projects and contributed to building data pipelines. Gained foundational experience in Python programming and statistical analysis.",
            start_date="Jan 2019",
            end_date="Dec 2019",
            location="Remote",
            company_url="https://loft.com.br"
        )
    ]
    return experiences


def seed_database():
    """Main function to seed the database with sample data"""
    print("🌱 Starting database seeding...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_projects = db.query(Project).count()
        existing_skills = db.query(Skill).count()
        existing_experiences = db.query(Experience).count()
        
        if existing_projects > 0 or existing_skills > 0 or existing_experiences > 0:
            print("⚠️  Database already contains data. Skipping seeding.")
            print(f"   Projects: {existing_projects}")
            print(f"   Skills: {existing_skills}")
            print(f"   Experiences: {existing_experiences}")
            return
        
        # Create and add sample projects
        print("📁 Creating sample projects...")
        projects = create_sample_projects()
        for project in projects:
            db.add(project)
        
        # Create and add sample skills
        print("🛠️  Creating sample skills...")
        skills = create_sample_skills()
        for skill in skills:
            db.add(skill)
        
        # Create and add sample experiences
        print("💼 Creating sample experiences...")
        experiences = create_sample_experiences()
        for experience in experiences:
            db.add(experience)
        
        # Commit all changes
        db.commit()
        
        print("✅ Database seeding completed successfully!")
        print(f"   Created {len(projects)} projects")
        print(f"   Created {len(skills)} skills")
        print(f"   Created {len(experiences)} experiences")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_database():
    """Clear all data from the database"""
    print("🗑️  Clearing database...")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Delete all records
        db.query(Experience).delete()
        db.query(Skill).delete()
        db.query(Project).delete()
        
        db.commit()
        print("✅ Database cleared successfully!")
        
    except Exception as e:
        print(f"❌ Error clearing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database seeding script")
    parser.add_argument(
        "--clear", 
        action="store_true", 
        help="Clear all data from the database before seeding"
    )
    parser.add_argument(
        "--clear-only", 
        action="store_true", 
        help="Only clear the database, don't seed new data"
    )
    
    args = parser.parse_args()
    
    try:
        if args.clear or args.clear_only:
            clear_database()
        
        if not args.clear_only:
            seed_database()
            
    except Exception as e:
        print(f"❌ Script failed: {e}")
        sys.exit(1)
