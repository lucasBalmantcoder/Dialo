from functools import wraps
from flask import request
import re

def sanitize_input(value: str) -> str:
    if not isinstance(value, str):
        return value
    value = re.sub(r'<[^>]*?>', '', value)              # remove HTML tags
    value = re.sub(r'[^\w@.\s-]', '', value)            # remove caracteres perigosos
    return value.strip()

def sanitize_json_fields(func):
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.is_json:
            sanitized = {}
            for key, val in request.get_json().items():
                if isinstance(val, str):
                    sanitized[key] = sanitize_input(val)
                else:
                    sanitized[key] = val
            request._cached_json = sanitized  # sobrescreve internamente
        return func(*args, **kwargs)
    return wrapper
