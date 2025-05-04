import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

CHANZO_AGENT_DB_NAME = os.getenv("CHANZO_AGENT_DB_NAME")
CHANZO_AGENT_DB_USER = os.getenv("CHANZO_AGENT_DB_USER")
CHANZO_AGENT_DB_PASSWORD = os.getenv("CHANZO_AGENT_DB_PASSWORD")
CHANZO_AGENT_DB_HOST = os.getenv("CHANZO_AGENT_DB_HOST")
CHANZO_AGENT_DB_PORT = os.getenv("CHANZO_AGENT_DB_PORT")

CHANZO_APP_DB_NAME = os.getenv("CHANZO_APP_DB_NAME")
CHANZO_APP_DB_USER = os.getenv("CHANZO_APP_DB_USER")
CHANZO_APP_DB_PASSWORD = os.getenv("CHANZO_APP_DB_PASSWORD")
CHANZO_APP_DB_HOST = os.getenv("CHANZO_APP_DB_HOST")
CHANZO_APP_DB_PORT = os.getenv("CHANZO_APP_DB_PORT")

chanzo_agent_db_url = f"mysql+mysqlconnector://{CHANZO_AGENT_DB_USER}:{CHANZO_AGENT_DB_PASSWORD}@{CHANZO_AGENT_DB_HOST}:{CHANZO_AGENT_DB_PORT}/{CHANZO_AGENT_DB_NAME}"
chanzo_agent_db_engine = create_engine(chanzo_agent_db_url)

chanzo_app_db_url = f"mysql+mysqlconnector://{CHANZO_APP_DB_USER}:{CHANZO_APP_DB_PASSWORD}@{CHANZO_APP_DB_HOST}:{CHANZO_APP_DB_PORT}/{CHANZO_APP_DB_NAME}"
chanzo_app_db_engine = create_engine(chanzo_app_db_url)
