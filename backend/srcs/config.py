import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("FLASK_DEBUG", False)
    JSON_SORT_KEYS = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:"
        f"{os.getenv('DB_PASSWORD', 'postgres')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '5432')}/"
        f"{os.getenv('DB_NAME', 'pt_elections')}"
    )


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('DB_HOST')}:"
        f"{os.getenv('DB_PORT')}/"
        f"{os.getenv('DB_NAME')}"
    )


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def get_config():
    """Get config based on environment"""
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        return ProductionConfig
    elif env == "testing":
        return TestingConfig
    else:
        return DevelopmentConfig
