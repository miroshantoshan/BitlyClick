import os
from typing import Dict, Optional

import requests
from dotenv import load_dotenv

load_dotenv()


def _get_token(token: Optional[str] = None) -> str:
    """
    Return the Bitly token from the argument or environment.
    Raises if no token is available.
    """
    if token:
        return token

    env_token = os.getenv("TOKEN_BITLY")
    if not env_token:
        raise RuntimeError("TOKEN_BITLY is not set; define it in .env or the environment")

    return env_token


def get_user_info(token: Optional[str] = None) -> Dict:
    token_value = _get_token(token)
    headers = {"Authorization": f"Bearer {token_value}"}
    response = requests.get("https://api-ssl.bitly.com/v4/user", headers=headers)
    response.raise_for_status()
    return response.json()


def short_link(long_url: str, token: Optional[str] = None) -> str:
    token_value = _get_token(token)
    headers = {
        "Authorization": f"Bearer {token_value}",
        "Content-Type": "application/json",
    }
    data = {"long_url": long_url}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/bitlinks",
        headers=headers,
        json=data,
    )
    response.raise_for_status()
    payload = response.json()
    return payload["link"]
