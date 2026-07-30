import os
import sys
import io
import time
import base64
import logging
import threading
import subprocess

import pyperclip
import keyboard

from dotenv import load_dotenv
from PIL import ImageGrab

from openrouter import ask

load_dotenv()

API_KEY = os.getenv("OPEN_ROUTER_KEY")
CONTEXT = os.getenv("CONTEXT")
MODEL = "stepfun/step-3.7-flash"
SHIFT_TIMEOUT = 1.5

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


class ScreenshotSolver:
    def __init__(self):
        if not API_KEY:
            raise ValueError("env OPEN_ROUTER_KEY not found!")
        if not CONTEXT:
            raise ValueError("env CONTEXT not found!")
        self.shift_times = []

    def clear_terminal(self):
        command = 'cls' if os.name == 'nt' else 'clear'
        subprocess.run(command, shell=True)

    def on_shift(self):
        now = time.time()
        self.shift_times = [t for t in self.shift_times if now - t < SHIFT_TIMEOUT]
        self.shift_times.append(now)
        if len(self.shift_times) >= 3:
            self.shift_times.clear()
            logger.info("Tripple Shift detected")
            threading.Thread(target=self.handle, daemon=True).start()

    def print_answer(self, answer):
        self.clear_terminal()
        print(answer)

    def handle(self):
        try:
            logger.info("Capturing...")
            img = ImageGrab.grab()
            buf = io.BytesIO()
            img.save(buf, format="JPEG", quality=85)
            b64 = base64.b64encode(buf.getvalue()).decode()
            logger.info("Captured: (%.0f KB)", len(b64) / 1024 * 0.75)
            logger.info("Sending to OpenRouter...")
            answer = ask(MODEL, CONTEXT, b64)

            self.print_answer(answer)

            if answer:
                pyperclip.copy(answer)
                print("Copied to clipboard")
            else:
                logger.error("Model error")

        except Exception as e:
            logger.exception("Model error")


if __name__ == "__main__":
    print("Start - Tripple Shift")
    print("Ctrl+C - Exit")
    print()

    solver = ScreenshotSolver()
    keyboard.on_press_key("shift", lambda e: solver.on_shift())
    logger.info("Running...")

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print()
        logger.info("Bye...")
        sys.exit(0)