import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=True)  # Nullable for Google OAuth users
    profile_picture = Column(String, nullable=True)
    provider = Column(String, nullable=False, default="local")  # "local" or "google"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Project(Base):
    __tablename__ = "projects"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ProjectVersion(Base):
    __tablename__ = "project_versions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"))
    version_tag = Column(String, nullable=False)
    concept = Column(JSONB, nullable=False)
    parent_version_id = Column(UUID(as_uuid=True), ForeignKey("project_versions.id"), nullable=True)
    iteration_reason = Column(String)
    
    agent_outputs = Column(JSONB)
    debate_history = Column(JSONB)
    battle_score = Column(JSONB)
    confidence_score = Column(JSONB)
    final_report = Column(JSONB)

class Run(Base):
    __tablename__ = "runs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_version_id = Column(UUID(as_uuid=True), ForeignKey("project_versions.id"), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=True)
    idea = Column(String, nullable=True)
    status = Column(String, nullable=False)
    final_state = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
