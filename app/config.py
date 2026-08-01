"""Environment-driven application configuration."""

import os


class Config:
    VERSION = os.getenv("APP_VERSION", "1.0.0")
    PORT = int(os.getenv("PORT", "5000"))
    DATABASE_PATH = os.getenv("DATABASE_PATH", "/data/students.db")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
