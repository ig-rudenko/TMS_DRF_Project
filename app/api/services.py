from typing import Callable, Any
from rest_framework.request import Request

from django.core.cache import cache


def get_cached_function(cache_key: str, timeout: int, function: Callable[[], Any]):
    data = cache.get(cache_key, None)
    if data is None:
        data = function()
        cache.set(cache_key, data, timeout)

    return data


def get_cached_posts_list(request: Request, function: Callable[[], Any]):
    cache_key = f"all_posts:{request.user}"
    cache_timeout = 10
    return get_cached_function(cache_key, cache_timeout, function)


def clean_cached_posts_list(request: Request):
    cache_key = f"all_posts:{request.user}"
    cache.delete(cache_key)
