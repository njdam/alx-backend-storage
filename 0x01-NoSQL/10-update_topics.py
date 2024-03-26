#!/usr/bin/env python3
""" Change school topics """


def update_topics(mongo_collection, name, topics):
    """
    A Python function that changes all topics of a school document
    based on the name!

    Args:
        mongo_collection: is pymongo collection object
        name (str): is the school name to update
        topics (list of str): is the list of topics approached in the school

    Returns:
        None
    """
    query = {"name": name}
    update = {"$set": {"topics": topics}}
    mongo_collection.update_many(query, update)
