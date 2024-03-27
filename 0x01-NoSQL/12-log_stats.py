#!/usr/bin/env python3
"""
A Python script that provides some stats about Nginx logs stored in MongoDB.

* Database: logs
* Collection: nginx
* Display (same as the example):
    first line: x logs where x is the number of documents in this collection
    second line: Methods:
    5 lines with the number of documents with the
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    in this order (see example below - warning: it’s a tabulation
    before each line)
    one line with the number of documents with:
        * method=GET
        * path=/status
"""

from pymongo import MongoClient


def log_stats():
    """
    Function that provides some stats about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Number of documents in the collection
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")

    # Methods
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Number of documents with method=GET and path=/status
    status_check_count = collection.count_documents(
            {"method": "GET", "path": "/status"}
            )
    print(f"{status_check_count} status check")


if __name__ == '__main__':
    log_stats()
