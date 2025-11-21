# backend/models.py
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between Project and Technology
project_technology = Table(
    'project_technology',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('technology_id', Integer, ForeignKey('technologies.id'))
)

class Hero(Base):
    __tablename__ = "hero"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    profession = Column(String(100))
    description = Column(Text)
    image = Column(String, nullable=True)

class About(Base):
    __tablename__ = "about"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    image = Column(String, nullable=True)

class Stats(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    value = Column(String)

    def __str__(self):
        return f"{self.title}: {self.value}"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True)
    
    technologies = relationship("Technology", back_populates="category")
    
    def __str__(self):
        return self.name

class Technology(Base):
    __tablename__ = "technologies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    proficiency = Column(Integer)  # Changed to Integer for percentage
    category_id = Column(Integer, ForeignKey("categories.id"))
    
    category = relationship("Category", back_populates="technologies")
    projects = relationship("Project", secondary=project_technology, back_populates="technologies")
    
    def __str__(self):
        return self.name

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150))
    description = Column(Text)
    technologies = relationship("Technology", secondary=project_technology, back_populates="projects")
    image = Column(String, nullable=True)
    link_demo = Column(String)
    link_git_github = Column(String)

class ContactAbout(Base):
    __tablename__ = "contact_about"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    icon = Column(String, nullable=True)
    
class ContactSocial(Base):
    __tablename__ = "contact_social"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String(100))
    link = Column(String(200))
    
class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    subject = Column(String(150))
    message = Column(Text)