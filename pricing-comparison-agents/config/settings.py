# config/settings.py

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient
import logging
import langchain

# Load environment variables from .env file
load_dotenv()
langchain.debug = True
# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration variables
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize model and client instances
model = ChatOpenAI(model=OPENAI_MODEL)
tavily = TavilyClient(api_key=TAVILY_API_KEY)  # Adjust according to TavilyClient's requirements
