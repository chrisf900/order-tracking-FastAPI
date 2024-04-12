import base64
from datetime import datetime


def encode_page_token(token: str):
    return base64.b64encode(token.encode()).decode()


def decode_page_token(token: str):
    decoded = base64.b64decode(token).decode().split("|")
    return datetime.fromisoformat(decoded[0])
