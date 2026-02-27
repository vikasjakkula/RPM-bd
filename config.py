import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.environ.get("PORT", 4000))
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    CORS_ORIGINS = True  # allow all origins for dev; set to ["http://localhost:3000"] for prod
