#!/usr/bin/env python3
""" Writing strings to Redis! """

import redis
import uuid
from typing import Union, Callable


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

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float
            ]:
        """
        Redis only allows to store string, bytes and numbers
        (and lists thereof). Whatever you store as single elements,
        it will be returned as a byte string.
        Hence if you store "a" as a UTF-8 string, it will be returned
        as b"a" when retrieved from the server.

        In this exercise we will create a get method that take a key string
        argument and an optional Callable argument named fn.
        This callable will be used to convert the data back
        to the desired format.

        Remember to conserve the original Redis.get behavior
        if the key does not exist.

        Also, implement 2 new methods: `get_str` and `get_int` that will
        automatically parametrize Cache.get with the correct conversion
        function.
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Union[str, None]:
        """
        It automatically parametrize Cache.get with the correct
        conversion function.
        """
        return self.get(key, fn=lambda x: x.decode('utf-8') if x else None)

    def get_int(self, key: str) -> Union[int, None]:
        """
        It automatically parametrize Cache.get with the correct
        conversion function.
        """
        return self.get(key, fn=lambda x: int(x) if x else None)
