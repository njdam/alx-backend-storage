#!/usr/bin/env python3
""" Python function that lists all documents in a collection! """


def list_all(mongo_collection):
    """
    Lists all documents in a MongoDB collection.

    Args:
        mongo_collection: PyMongo collection object.

    Returns:
        list: List of documents in the collection.
    """
    return list(mongo_collection.find())
