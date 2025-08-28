from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from .database import Base


class Project(Base):
    """Local projects model"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    technologies = Column(String(500))  # Comma-separated list
    github_url = Column(String(500))
    demo_url = Column(String(500))
    image_url = Column(String(500))
    featured = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Contact(Base):
    """Contact form submissions"""
    __tablename__ = "contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Skill(Base):
    """Skills for resume section"""
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # e.g., "programming", "tools", "frameworks"
    proficiency = Column(Integer)  # 1-5 scale
    icon_name = Column(String(50))  # For icon display
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Experience(Base):
    """Work experience for resume"""
    __tablename__ = "experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)
    description = Column(Text)
    start_date = Column(String(20))  # e.g., "Jan 2023"
    end_date = Column(String(20))  # e.g., "Present"
    location = Column(String(100))
    company_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
