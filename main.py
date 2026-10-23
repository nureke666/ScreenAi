import google.generativeai as genai
import anthropic
from PIL import ImageGrab
import os
import io
import base64
import itertools
import time
import re
from config import (
    SAVE_FOLDER,
    X_COORD,
    Y_COORD,
    WIDTH,
    HEIGHT,
    GEMINI_KEYS,
    CLAUDE_KEY,
    GEMINI_MODEL,
    CLAUDE_MODEL,
    PROMPT
)

# Инициализация цикла ключей Gemini
if GEMINI_KEYS:
    gemini_key_cycle = itertools.cycle(GEMINI_KEYS)
else:
    gemini_key_cycle = None
    print("⚠️  Внимание: Ключи Gemini не найдены в .env")


def get_next_filename():
    """Находит следующий номер для сохранения файла."""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        return os.path.join(SAVE_FOLDER, "1.jpg")

    files = [f for f in os.listdir(SAVE_FOLDER) if f.endswith(".jpg")]
    max_num = 0
    for f in files:
        try:
            num = int(os.path.splitext(f)[0])
            if num > max_num: max_num = num
        except ValueError:
            continue
    return os.path.join(SAVE_FOLDER, f"{max_num + 1}.jpg")


def encode_image_to_base64(screenshot):
    """Конвертация в base64 для Claude."""
    buffered = io.BytesIO()
    screenshot.save(buffered, format="JPEG", quality=85)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def take_screenshot():
    """Скриншот области экрана."""
    print(f"\n📸 Делаю скриншот...")
    try:
        screenshot = ImageGrab.grab(bbox=(X_COORD, Y_COORD, X_COORD + WIDTH, Y_COORD + HEIGHT)).convert("RGB")
        save_path = get_next_filename()
        screenshot.save(save_path)
        print(f"✅ Сохранено: {save_path}")
        return screenshot
    except Exception as e:
        print(f"❌ Ошибка скриншота: {e}")
        return None


def extract_answer(text):
    """Пытается извлечь только позицию варианта ответа: 1, 2, 3 или 4."""
    if not text:
        return None
    text = str(text).strip()
    match = re.search(r"\b[1-4]\b", text)
    if match:
        return match.group(0)
    return None


def run_gemini(screenshot):
    """Запрос к Gemini с ротацией ключей."""
    if not gemini_key_cycle:
        print("❌ Нет ключей Gemini.")
        return

    try:
        current_key = next(gemini_key_cycle)
        genai.configure(api_key=current_key)
        model = genai.GenerativeModel(GEMINI_MODEL)

        print(f"🚀 Запрос к {GEMINI_MODEL}...")
        response = model.generate_content([PROMPT, screenshot])

        raw_text = response.text if response.text else ""
        answer = extract_answer(raw_text)

        print("\n" + "=" * 10 + " GEMINI " + "=" * 10)
        if answer:
            print(answer)
        else:
            print(raw_text if raw_text else "⚠️ Пустой ответ (фильтр?)")
            print("⚠️ Не удалось однозначно извлечь вариант ответа. Проверьте формат или попробуйте другой ключ.")
        print("=" * 28 + "\n")

    except Exception as e:
        print(f"❌ Ошибка Gemini: {e}")


def run_claude(screenshot):
    """Запрос к Claude."""
    if not CLAUDE_KEY:
        print("❌ Нет ключа Claude.")
        return

    try:
        client = anthropic.Anthropic(api_key=CLAUDE_KEY)
        base64_image = encode_image_to_base64(screenshot)

        print(f"🚀 Запрос к {CLAUDE_MODEL}...")
        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": [
                    {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": base64_image}},
                    {"type": "text", "text": PROMPT}
                ]
            }]
        )
        raw_text = ""
        if response.content and len(response.content) > 0:
            first_content = response.content[0]
            if isinstance(first_content, dict):
                raw_text = first_content.get("text", "") or ""
            else:
                raw_text = getattr(first_content, 'text', '') or ''
        answer = extract_answer(raw_text)

        print("\n" + "=" * 10 + " CLAUDE " + "=" * 10)
        if answer:
            print(answer)
        else:
            print(raw_text if raw_text else "⚠️ Пустой ответ (фильтр?)")
            print("⚠️ Не удалось однозначно извлечь вариант ответа. Проверьте формат или попробуйте другой ключ.")
        print("=" * 28 + "\n")

    except Exception as e:
        print(f"❌ Ошибка Claude: {e}")


def main():
    current_mode = None

    print("\n🔮 AI Screenshot Helper")

    while True:
        if current_mode is None:
            print("\nВыбери режим:")
            print("1. Google Gemini (Ротация ключей)")
            print("2. Claude 3.5 Sonnet")
            choice = input(">> ").strip()

            if choice == "1":
                current_mode = "gemini"
            elif choice == "2":
                current_mode = "claude"
            else:
                continue
            print(f"✅ Режим: {current_mode.upper()}")

        user_input = input(f"[{current_mode.upper()}] Enter=Скриншот | 'm'=Меню | 'q'=Выход: ").lower().strip()

        if user_input == 'q':
            break
        if user_input in ['m', 'menu', 'ь']:
            current_mode = None
            continue

        screenshot = take_screenshot()
        if screenshot:
            if current_mode == "gemini":
                run_gemini(screenshot)
            elif current_mode == "claude":
                run_claude(screenshot)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Выход.")