import datetime

from django.core.cache import cache


def badi_cache(**decorator_kwargs):
    def decorator(func):
        def wrapper(*args, **kwargs):
            timeout = decorator_kwargs.get('timeout', 30)
            key = decorator_kwargs.get('key', func.__name__)
            data = cache.get(key)
            if not data:
                data = func(*args, **kwargs)
                cache.set(key, data, timeout)
            return data

        return wrapper

    return decorator
