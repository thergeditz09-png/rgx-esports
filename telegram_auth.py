import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from config import BOT_TOKEN


def verify_telegram_init_data(init_data: str):
    if not BOT_TOKEN or not init_data:
        return None

    try:
        values = dict(parse_qsl(init_data, keep_blank_values=True))
        received_hash = values.pop("hash", None)

        if not received_hash:
            return None

        data_check_string = "\n".join(
            f"{key}={value}"
            for key, value in sorted(values.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            BOT_TOKEN.encode(),
            hashlib.sha256
        ).digest()

        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(calculated_hash, received_hash):
            return None

        auth_date = int(values.get("auth_date", "0"))

        if time.time() - auth_date > 3600 or auth_date > time.time() + 60:
            return None

        user = json.loads(values.get("user", "{}"))

        if not isinstance(user.get("id"), int):
            return None

        return user

    except (ValueError, TypeError, json.JSONDecodeError):
        return None
