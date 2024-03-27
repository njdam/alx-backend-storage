#!/usr/bin/env python3
""" Where can I learn Python? """


def schools_by_topic(mongo_collection, topic):
    """
    A Python function that returns the list of school having
    a specific topic!

    Args:
        mongo_collection: is the pymongo collection object
        topic (str): is a topic to be searched

    Returns:
        list: List of schools matching the specified topic.
    """
    query = {"topics": topic}
    schools = mongo_collection.find(query)
    return list(schools)
