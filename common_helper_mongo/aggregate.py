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
