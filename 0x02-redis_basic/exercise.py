#!/usr/bin/env python3
""" Writing strings to Redis! """

import redis
import uuid
from typing import Union


class Cache:
    """
    A Cache class with `__init__` method, store an instance of the Redis
    client as a private variable named `_redis` (using `redis.Redis()`)
    and flush the instance using `flushdb`.

    And with a `store` method that takes a data argument
    and returns a string. The method should generate a random key
    (e.g. using `uuid`), store the input data in Redis using the random key
    and return the key.

    Type-annotate store correctly. Remember that data can be a `str`,
    `bytes`, `int` or `float`.
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()  # Clear the Redis database

    def store(self, data: Union[str, bytes, int, float]) -> str:
        rand_key = str(uuid.uuid4())  # To Generate a random key
        self._redis.set(rand_key, data)  # To store data in Redis

        return rand_key
