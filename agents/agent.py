import os
from dotenv import load_dotenv
from llama_index.llms.gemini import Gemini
from llama_index.core import Settings
from llama_index.core.agent import ReActAgent

load_dotenv()

TOKEN=os.getenv("TELEGRAM_BOT")
GEMINI_KEY = os.getenv("GEMINI_KEY")


llm = Gemini(
    model="models/gemini-1.5-flash",
    api_key=GEMINI_KEY
)


Settings.llm = llm

