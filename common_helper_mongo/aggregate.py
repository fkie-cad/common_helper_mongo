import logging
from bson.son import SON


def get_objects_and_count_of_occurrence(collection, object_path, unwind=False, match=None):
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
    return get_field_execute_operation("$sum", collection, object_path, match=match)


def get_field_average(collection, object_path, match=None):
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
