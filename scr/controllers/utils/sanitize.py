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
            
            # A correção é atribuir os dados sanitizados à chave 'False'
            # dentro do _cached_json. Isso simula o comportamento interno do Flask.
            request._cached_json = {False: sanitized} # <-- CORREÇÃO AQUI
            
            # Opcional: Se você quiser garantir que o request.json seja atualizado
            # de forma mais direta, você pode usar uma solução como:
            # from werkzeug.wrappers import Request
            # request.__class__.json = property(lambda self: sanitized)
            # Mas a sobrescrita de _cached_json é o método mais comum para este caso.
        return func(*args, **kwargs)
    return wrapper
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
            
            # A correção é atribuir os dados sanitizados à chave 'False'
            # dentro do _cached_json. Isso simula o comportamento interno do Flask.
            request._cached_json = {False: sanitized} # <-- CORREÇÃO AQUI
            
            # Opcional: Se você quiser garantir que o request.json seja atualizado
            # de forma mais direta, você pode usar uma solução como:
            # from werkzeug.wrappers import Request
            # request.__class__.json = property(lambda self: sanitized)
            # Mas a sobrescrita de _cached_json é o método mais comum para este caso.
        return func(*args, **kwargs)
    return wrapper
