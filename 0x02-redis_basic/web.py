#!/usr/bin/env python3
'''A module with tools for request caching and tracking.
'''
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
'''The module-level Redis instance.
'''


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text


'''
#!/usr/bin/env python3
"""
A module with tools for request caching and tracking.
"""

import redis
import requests
from functools import wraps
from typing import Callable
import threading


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
        redis_client.set(f'count:{url}', 0)

        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    return requests.get(url).text
'''
