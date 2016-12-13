import logging
from bson.son import SON


def get_objects_and_count_of_occurrence(collection, object_path, unwind=False, match=None):
    """
    Get a list of unique values and their occurences on a specific object path in a collection.
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection
    :param object_path: mongo object path
    :type object_path: str
    :param unwind: if true: handle list entries as single values
    :type unwind: bool
    :param match: mongo search string
    :type match: dict
    :return: [{'_id': <VALUE>, 'count': <OCCURENCES>}, ...]
    """
    pipeline = []
    if match is not None:
        pipeline.append({"$match": match})
    pipeline.extend([
        {"$group": {"_id": object_path, "count": {"$sum": 1}}},
        {"$sort": SON([("count", -1), ("_id", -1)])}
        ])
    if unwind:
        old_pipe = pipeline
        pipeline = [{"$unwind": object_path}]
        pipeline.extend(old_pipe)
    result = list(collection.aggregate(pipeline))
    logging.debug(result)
    return result


def get_field_sum(collection, object_path, match=None):
    """
    Get sum of all values in this field
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection
    :param object_path: mongo object path
    :type object_path: str
    :param match: mongo search string
    :type match: dict
    :return: int
    """
    return get_field_execute_operation("$sum", collection, object_path, match=match)


def get_field_average(collection, object_path, match=None):
    """
    Get average of all values in this field
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection
    :param object_path: mongo object path
    :type object_path: str
    :param match: mongo search string
    :type match: dict
    :return: float
    """
    return get_field_execute_operation("$avg", collection, object_path, match=match)


def get_field_execute_operation(operation, collection, object_path, match=None):
    pipeline = []
    if match is not None:
        pipeline.append({"$match": match})
    pipeline.append({"$group": {"_id": "null", "total": {operation: object_path}}})
    tmp = collection.aggregate(pipeline)
    result = 0
    for item in tmp:
        result = item['total']
    return result
