#!/usr/bin/env python3
"""
Log stats - new version that Improve 12-log_stats.py by adding the top 10
of the most present IPs in the collection nginx of the database logs

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
    """
    or This if you don't know methods
    # Count the occurrence of each HTTP method
    method_stats = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])
    print("Methods:")
    for method_stat in method_stats:
        print(f"    method {method_stat['_id']}: {method_stat['count']}")
    """
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

    # Count the occurrence of each IP address and get the top 10
    ip_stats = collection.aggregate([
            {
                "$group": {"_id": "$ip", "count": {"$sum": 1}}
                },
            {
                "$sort": {"count": -1}
                },
            {
                "$limit": 10
                }
            ])
    print("IPs:")
    for ip_stat in ip_stats:
        print(f"\t{ip_stat['_id']}: {ip_stat['count']}")


if __name__ == '__main__':
    log_stats()
