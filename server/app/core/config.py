# from pydantic_settings import BaseSettings
# from typing import Optional

# class Settings(BaseSettings):
#     PROJECT_NAME: str = "Church Management System"
#     VERSION: str = "1.0.0"
#     API_V1_STR: str = "/api/v1"
    
#     # Security
#     SECRET_KEY: str = "your-secret-key-here"  # Change this in production
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
#     # Database
#     # DATABASE_URL: str = "sqlite:///./church_management.db"
    
#     # SMTP Settings
#     SMTP_HOST: str = 'smtp.mailtrap.io'  # Standard Mailtrap host
#     SMTP_PORT: int = 2525  # Standard Mailtrap port
#     SMTP_USERNAME: str = ""  # Set this in .env file
#     SMTP_PASSWORD: str = ""  # Set this in .env file
    
#     class Config:
#         case_sensitive = True
#         env_file = ".env"

# settings = Settings() 