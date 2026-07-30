import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

API_KEY = os.getenv("OPEN_ROUTER_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
SITE_URL = "https://github.com/denistol/iw-utils"
SITE_NAME = "iw-utils"


def ask(model: str, context: str, image_b64: str) -> str | None:

    if not API_KEY:
        logger.error("OPEN_ROUTER_KEY not found")
        return None

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": SITE_URL,
        "X-Title": SITE_NAME,
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": context},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                    },
                ],
            }
        ],
        "max_tokens": 4096,
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()

    except requests.Timeout:
        logger.error("Timeout OpenRouter")
        return None
    except requests.RequestException as e:
        logger.error("Ошибка API: %s", e)
        if hasattr(e, "response") and e.response is not None:
            logger.error("Тело ответа: %s", e.response.text[:500])
        return None
    except (KeyError, IndexError, ValueError) as e:
        logger.error("Неожиданный ответ API: %s", e)
        return None