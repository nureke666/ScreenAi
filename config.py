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
PROMPT = (
    "На скриншоте викторина: вопрос в центре и 4 варианта ответа расположены вертикально.\n"
    "Варианты расположены так: 1-й вверху, 2-й, 3-й, 4-й внизу.\n"
    "\n"
    "Твоя задача:\n"
    "1. Внимательно прочитай вопрос\n"
    "2. Выбери из 4 вариантов ТОЛЬКО правильный ответ\n"
    "3. Выведи ТОЛЬКО одну цифру (1, 2, 3 или 4) соответствующую позиции правильного варианта\n"
    "\n"
    "ТРЕБОВАНИЯ К ОТВЕТУ:\n"
    "- Только одна цифра: 1, 2, 3 или 4\n"
    "- БЕЗ букв, букв (A, B, C, D) или каких-либо других символов\n"
    "- БЕЗ слов 'Ответ:', 'вариант', пояснений или комментариев\n"
    "- БЕЗ переносов строк\n"
    "\n"
    "Пример ответа: 2"
)