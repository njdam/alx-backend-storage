#!/usr/bin/env python3
""" Insert a document in Python """


def insert_school(mongo_collection, **kwargs):
    """
    A Python function that inserts a new document in a collection
    based on kwargs

    Args:
        mongo_collection: PyMongo collection object.
        **kwargs: Keyword arguments representing the fields and
            values of the document to be inserted.

    Returns:
        str: The _id of the newly inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
