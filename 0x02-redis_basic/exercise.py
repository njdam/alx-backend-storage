#!/usr/bin/env python3
""" Writing strings to Redis! """

import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Familiarize yourself with the `INCR` command and its python equivalent.

    Implementation of a system to count how many times methods
    of the Cache class are called.

    Above Cache to define a count_calls decorator that takes a single
    `method` `Callable` argument and returns a `Callable`.

    As a key, use the qualified name of method using the `__qualname__`
    dunder method.

    Create and return function that increments the count for that `key`
    every time the method is called and returns the value returned
    by the original method.

    Remember that the first argument of the wrapped function will be `self`
    which is the instance itself, which lets you access the Redis instance.

    Protip: when defining a decorator it is useful to use `functool.wraps`
    to conserve the original function’s name, docstring, etc.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        key = method.__qualname__
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Familiarize yourself with redis commands `RPUSH`, `LPUSH`, `LRANGE`, etc

    In this task, we will define a `call_history` decorator to store
    the history of inputs and outputs for a particular function.

    Everytime the original function will be called, we will add its input
    parameters to one list in redis, and store its output into another list.

    In `call_history`, use the decorated function’s qualified name
    and append `":inputs"` and `":outputs"` to create input and output
    list keys, respectively.

    `call_history` has a single parameter named method that is a `Callable`
    and returns a `Callable`.

    In the new function that the decorator will return, use `rpush`
    to append the input arguments. Remember that Redis can only store
    strings, bytes and numbers. Therefore, we can simply use `str(args)`
    to normalize. We can ignore potential `kwargs` for now.

    Execute the wrapped function to retrieve the output. Store the output
    using `rpush` in the `"...:outputs"` list, then return the `output`.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Append input arguments to the inputs list
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output in the outputs list
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


def replay(fn: Callable) -> None:
    """
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_client = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_client, redis.Redis):
        return
    fxn_name = fn.__qualname__  # or method name
    input_key = fxn_name + ":inputs"
    output_key = fxn_name + ":outputs"

    fxn_call_count = 0
    if redis_client.exists(fxn_name) != 0:
        fxn_call_count = int(redis_client.get(fxn_name))

    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    # fxn_call_count or {len(inputs)}
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))

    for input_args, output in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(
            fxn_name,
            input_args.decode('utf-8'),
            output.decode('utf-8'),
        ))


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

    @call_history  # Decorate Cache.store with call_history
    @count_calls  # Decorate Cache.store with count_calls
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
