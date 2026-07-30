# Screenshot Solver

A lightweight Windows tool that takes a screenshot when you press **Shift 3 times** and sends it to an AI model via OpenRouter to solve the task shown on screen.

## How it works

1. Run the script (it stays in the background)
2. Press **Shift** 3 times quickly (within 1.5 seconds)
3. A screenshot is captured and sent to OpenRouter
4. The AI response is printed to the console and **copied to clipboard**

## Requirements

- Python 3.10+
- OpenRouter API key

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
echo OPEN_ROUTER_KEY=sk-or-v1-your-key-here > .env
echo CONTEXT=Find the task on the screen and solve it >> .env
```

## Usage

```bash
python main.py
```

> ⚠️ **Run as Administrator** — the `keyboard` library needs admin rights to detect global key presses.

Press **Ctrl+C** to exit.

## Files

| File | Description |
|------|-------------|
| `main.py` | Main script — listens for triple Shift, captures screenshot, calls API |
| `openrouter.py` | OpenRouter API client — sends images and returns AI responses |
| `.env` | API key and context prompt (not committed to git) |
| `requirements.txt` | Python dependencies |