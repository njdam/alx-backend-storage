#!/usr/bin/env python3
""" Top students """


def top_students(mongo_collection):
    """
    A Python function that returns all students sorted by average score

    Args:
        mongo_collection: is the pymongo collection object

    Returns:
        top_students (list): list of all students sorted by average score
    """
    pipeline = [
            {
                "$project": {  # creating computed fields
                    "name": 1,  # Reamain unchanged
                    "topics": 1,  # Reamain unchanged & calculate average score
                    "averageScore": {"$avg": "$topics.score"}
                }
            },
            {
                "$sort": {"averageScore": -1}  # In descending order (`-1`)
            }
        ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
