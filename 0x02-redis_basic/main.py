#!/usr/bin/env python3
"""
Main file
"""
import redis

Cache = __import__('exercise').Cache
replay = __import__('exercise').replay
get_page = __import__('web').get_page

cache = Cache()

# Mandatory Tasks
print("--------------------------------------------------------------")
print("Mandatory Tasks")
print("--------------------------------------------------------------")
print("\nTask 0\n")
data = b"hello"
key = cache.store(data)
print(key)

local_redis = redis.Redis()
print(local_redis.get(key))

print("--------------------------------------------------------------")
print("\nTask 1\n")
TEST_CASES = {
    b"foo": None,
    123: int,
    "bar": lambda d: d.decode("utf-8")
}

for value, fn in TEST_CASES.items():
    key = cache.store(value)
    assert cache.get(key, fn=fn) == value  # To check if no error
    print(cache.get(key, fn=fn) == value)  # ToPrint for always True results

print("--------------------------------------------------------------")
print("\nTask 2\n")
cache.store(b"first")
print(cache.get(cache.store.__qualname__))

cache.store(b"second")
cache.store(b"third")
print(cache.get(cache.store.__qualname__))

print("--------------------------------------------------------------")
print("\nTask 3\n")
s1 = cache.store("first")
print(s1)
s2 = cache.store("secont")
print(s2)
s3 = cache.store("third")
print(s3)

inputs = cache._redis.lrange(
        "{}:inputs".format(cache.store.__qualname__), 0, -1)
outputs = cache._redis.lrange(
        "{}:outputs".format(cache.store.__qualname__), 0, -1)

print("inputs: {}".format(inputs))
print("outputs: {}".format(outputs))

print("--------------------------------------------------------------")
print("\nTask 4\n")
cache.store("foo")
cache.store("bar")
cache.store(42)

replay(cache.store)

print("--------------------------------------------------------------")
# Advanced Tasks
print("--------------------------------------------------------------")
print("Advanced Tasks")
print("\nTask 5\n")
# Test the get_page function and Test for track_url_access_count decorator
url = (
        "http://slowwly.robertomurray.co.uk/delay/10000/url/"
        "http://www.example.com"
        )

local_redis = redis.Redis()
# Access count before calling get_page
initial_count = local_redis.get(f"count:{url}")
if initial_count is not None:
    initial_count = int(initial_count)
else:
    initial_count = 0
print(f"Initial access count for {url}: {initial_count}")
print("")
# Call get_page function
content = get_page(url)
print(f"Content retrieved for {url}:\n{content}")
content = get_page(url)
content = get_page(url)
content = get_page(url)

# Access count after calling get_page
updated_count = local_redis.get(f"count:{url}")
if updated_count is not None:
    updated_count = int(updated_count)
else:
    updated_count = 0
print(f"Updated access count for {url}: {updated_count}")
print("")
