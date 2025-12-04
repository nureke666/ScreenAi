# ScreenAI

A Python tool designed to quickly solve on-screen questions using AI models (Google Gemini or Claude 3.5 Sonnet). It captures a specific region of your screen, sends the image to the selected API, and returns the answer.

## ⚡️ Installation (via uv)

This project uses the `uv` package manager.

1. **Initialize the project (if starting fresh):**
   ```bash
   uv init
   ```

2. **Install dependencies:**
   Run the following command to add the required libraries:
   ```bash
   uv add google-generativeai anthropic python-dotenv pyautogui pillow
   ```

## ⚙️ Configuration

### 1. API Keys
Create a `.env` file in the root directory and add your API keys.
*   **Gemini:** You can add up to 3 keys. The script rotates through them automatically to avoid rate limits.
*   **Claude:** Requires a single key.

```env
GEMINI_API_KEY_1=your_gemini_key_1
GEMINI_API_KEY_2=your_gemini_key_2
GEMINI_API_KEY_3=your_gemini_key_3
CLAUDE_API_KEY=your_claude_key
```

### 2. Screen Coordinates
Open `config.py` to adjust the screenshot area.
Modify these values to match the screen region where your questions appear:

```python
X_COORD = 0      # X position (top-left)
Y_COORD = 0      # Y position (top-left)
WIDTH = 960      # Width of the capture area
HEIGHT = 1080    # Height of the capture area
```

*Tip: If you are using a standard 1920x1080 monitor and want to capture the left half, the default settings are already correct.*

## 🚀 Usage

Run the script using `uv`:

```bash
uv run main.py
```

For connect smaptphone need to use usb and command:
```bash
/snap/bin/scrcpy
```
## 🎮 Controls

1. **Select Model:** At startup, choose **1** (Gemini) or **2** (Claude).
2. **Capture & Solve:** Press **Enter** to take a screenshot and get the answer.
3. **Change Model:** Type **m** (or menu) and press Enter to switch the AI model.
4. **Quit:** Type **q** and press Enter to exit.

All screenshots are automatically saved to the `saved_screenshots` folder for reference.
