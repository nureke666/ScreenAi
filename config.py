import os
from dotenv import load_dotenv

load_dotenv()

# Folder for screenshots
SAVE_FOLDER = "saved_screenshots"

# Settings of Screenshot
X_COORD = 0
Y_COORD = 0
WIDTH = 960
HEIGHT = 1080

# API
GEMINI_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]
GEMINI_KEYS = [k for k in GEMINI_KEYS if k]

CLAUDE_KEY = os.getenv("CLAUDE_API_KEY")

# Models
GEMINI_MODEL = "gemini-2.5-flash"
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"

# Prompt
PROMPT = "Посмотри на скриншот. Внимательно прочитай вопрос и варианты. Выдай ТОЛЬКО правильный ответ (букву или цифру). Без лишних слов."