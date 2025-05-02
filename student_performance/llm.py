import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

deepseek_model = "deepseek-chat"
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
os.environ["DEEPSEEK_API_KEY"] = DEEPSEEK_API_KEY

llm = ChatDeepSeek(model=deepseek_model)
