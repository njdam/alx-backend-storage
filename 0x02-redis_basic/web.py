#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import redis
import requests
from functools import wraps
from typing import Callable


# Redis client
redis_client = redis.Redis()


def data_cacher(func: Callable) -> Callable:
    """
    Caches the output of fetched data.
    """
    @wraps(func)
    def wrapper(url) -> str:
        """
        The wrapper function for caching the output.
        """
        # Increment access count for the URL
        redis_client.incr(f'count:{url}')

        # Try to get cached result
        cached_result = redis_client.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        # Call the original function
        result = func(url)

        # Cache the result with expiration time of 10 seconds
        redis_client.setex(f'result:{url}', 10, result)

        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    response = requests.get(url)
    return response.text
