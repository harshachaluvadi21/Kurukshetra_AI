from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
import os

# Resolve the path to .env dynamically relative to this file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

class Settings(BaseSettings):
    environment: str = Field(default="development", alias="ENVIRONMENT")
    
    # LLM
    google_api_key: str = Field(..., alias="GOOGLE_API_KEY")
    groq_api_key: Optional[str] = Field(None, alias="GROQ_API_KEY")
    
    # Search
    tavily_api_key: str = Field(..., alias="TAVILY_API_KEY")
    serper_api_key: str = Field(..., alias="SERPER_API_KEY")
    
    # Database
    database_url: str = Field(..., alias="DATABASE_URL")
    
    # RAG (Chroma)
    chroma_persist_directory: str = Field(..., alias="CHROMA_PERSIST_DIRECTORY")
    chroma_host: Optional[str] = Field(None, alias="CHROMA_HOST")
    chroma_api_key: Optional[str] = Field(None, alias="CHROMA_API_KEY")
    chroma_tenant: Optional[str] = Field(None, alias="CHROMA_TENANT")
    chroma_database: Optional[str] = Field(None, alias="CHROMA_DATABASE")
    
    # LangSmith Tracing
    langchain_api_key: Optional[str] = Field(None, alias="LANGCHAIN_API_KEY")
    langchain_tracing_v2: Optional[str] = Field(None, alias="LANGCHAIN_TRACING_V2")
    
    # Battle Score Weights
    WEIGHT_MARKET_OPPORTUNITY: float = 0.20
    WEIGHT_COMPETITION_DIFFICULTY: float = 0.15
    WEIGHT_REVENUE_POTENTIAL: float = 0.20
    WEIGHT_EXECUTION_COMPLEXITY: float = 0.10
    WEIGHT_INVESTMENT_READINESS: float = 0.20
    WEIGHT_RISK_LEVEL: float = 0.15
    
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")

    def validate_health(self):
        """Validates critical infrastructure configurations and reports status."""
        print("==========================================================")
        print(" SYSTEM HEALTH CHECK ")
        print("==========================================================")
        
        status = {
            "Gemini": "PASS" if self.google_api_key else "FAIL (Missing GOOGLE_API_KEY)",
            "Groq": "PASS" if self.groq_api_key else "WARNING (Missing GROQ_API_KEY - Fallback Disabled)",
            "Tavily": "PASS" if self.tavily_api_key else "FAIL (Missing TAVILY_API_KEY)",
            "Serper": "PASS" if self.serper_api_key else "FAIL (Missing SERPER_API_KEY)",
            "PostgreSQL": "PASS" if self.database_url else "FAIL (Missing DATABASE_URL)",
            "Chroma": "PASS" if self.chroma_host and self.chroma_api_key else "WARNING (Local Fallback)",
            "LangSmith": "PASS" if self.langchain_api_key and self.langchain_tracing_v2 == "true" else "WARNING (Tracing Disabled)"
        }
        
        for component, result in status.items():
            print(f"{component:12} | {result}")
            
        print("==========================================================")
        
        # Fail fast if critical deps are missing
        if not self.google_api_key or not self.tavily_api_key or not self.serper_api_key or not self.database_url:
            raise ValueError("Critical configuration is missing. Cannot start Kurukshetra AI.")

settings = Settings()
