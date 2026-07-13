# Configuration settings
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Determine base directory (works for both development and packaged EXE)
if getattr(sys, "frozen", False):
    # Running as compiled EXE
    BASE_DIR = Path(sys.executable).parent
else:
    # Running as Python script
    BASE_DIR = Path(__file__).resolve().parent

# Load .env from base directory
env_path = BASE_DIR / ".env"
load_dotenv(env_path)

SOURCE_URL = os.getenv("SOURCE_URL")
SOURCE_USERNAME = os.getenv("SOURCE_USERNAME")
SOURCE_PASSWORD = os.getenv("SOURCE_PASSWORD")

TARGET_URL = os.getenv("TARGET_URL")
TARGET_USERNAME = os.getenv("TARGET_USERNAME")
TARGET_PASSWORD = os.getenv("TARGET_PASSWORD")