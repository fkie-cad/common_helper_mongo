import logging
from typing import List, Optional

from bson.son import SON


def get_list_of_all_values(collection, object_path, unwind=False, match=None):
    '''
    Get a list of unique values on a specific object path in a collection.
    An Optional search string (match) can be added.
    If additional_field is set, all values of this field for each

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param object_path: mongo object path
    :type object_path: str
    :param unwind: if true: handle list entries as single values
    :type unwind: bool
    :param match: mongo search string
    :type match: dict, optional
    :return: list
    '''
    pipeline = _build_pipeline(object_path, {'_id': object_path}, unwind, SON([('_id', 1)]), match)
    result = _get_list_of_aggregate_list(list(collection.aggregate(pipeline)))
    logging.debug(result)
    return result


def get_list_of_all_values_and_collect_information_of_additional_field(
        collection, object_path, additional_information_object_path, unwind=False, match=None):
    '''
    Get a list of unique values and a collection of additional information on a specific object path in a collection.
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param object_path: mongo object path
    :type object_path: str
    :param additional_information_object_path: field of the additional information
    :type additional_information_object_path: str
    :param unwind: if true: handle list entries as single values
    :type unwind: bool
    :param match: mongo search string
    :type match: dict, optional
    :return: {<VALUE>:[<ADDITIONAL_INFORMATION_1>, ...], ...}
    '''
    logging.warning('deprecation warning: this method will be removed in a future release')
    return get_all_value_combinations_of_fields(collection, object_path, additional_information_object_path, unwind, match)


def get_all_value_combinations_of_fields(collection, primary_field, secondary_field, unwind=False, match=None):
    '''
    Get a dictionary with all unique values of a field as keys and a list of all unique values that a second field takes
    on as values (on a specific object path in a collection). An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param primary_field: mongo object path
    :type primary_field: str
    :param secondary_field: field of the additional information
    :type secondary_field: str
    :param unwind: if true: handle list entries as single values
    :type unwind: bool
    :param match: mongo search string
    :type match: dict, optional
    :return: {<VALUE>:[<ADDITIONAL_INFORMATION_1>, ...], ...}
    '''
    pipeline = _build_pipeline(
        primary_field, {'_id': primary_field, 'additional_information': {'$addToSet': secondary_field}},
        unwind, SON([('_id', 1)]), match
    )
    result = list(collection.aggregate(pipeline))
    result = _get_dict_from_aggregate_list(result)
    logging.debug(result)
    return result


def _get_dict_from_aggregate_list(ag_list):
    result = {}
    for item in ag_list:
        result[item['_id']] = item['additional_information']
    return result


def _get_list_of_aggregate_list(ag_list):
    return [item['_id'] for item in ag_list]


def get_objects_and_count_of_occurrence(collection, object_path, unwind=False, match=None):
    '''
    Get a list of unique values and their occurrences on a specific object path in a collection.
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param object_path: mongo object path
    :type object_path: str
    :param unwind: if true: handle list entries as single values
    :type unwind: bool
    :param match: mongo search string
    :type match: dict, optional
    :return: [{'_id': <VALUE>, 'count': <OCCURRENCES>}, ...]
    '''
    pipeline = _build_pipeline(object_path, {'_id': object_path, 'count': {'$sum': 1}}, unwind,
                               SON([('count', -1), ('_id', -1)]), match)
    result = list(collection.aggregate(pipeline))
    logging.debug(result)
    return result


def get_field_sum(collection, object_path, match=None):
    '''
    Get sum of all values in this field
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param object_path: mongo object path
    :type object_path: str
    :param match: mongo search string
    :type match: dict
    :return: int
    '''
    return get_field_execute_operation('$sum', collection, object_path, match=match)


def get_field_average(collection, object_path, match=None):
    '''
    Get average of all values in this field
    An Optional search string (match) can be added.

    :param collection: mongo collection to look at
    :type collection: pymongo.collection.Collection
    :param object_path: mongo object path
    :type object_path: str
    :param match: mongo search string
    :type match: dict
    :return: float
    '''
    return get_field_execute_operation('$avg', collection, object_path, match=match)


def get_field_execute_operation(operation, collection, object_path, match=None):
    pipeline = _build_pipeline(object_path, {'_id': 'null', 'total': {operation: object_path}}, match=match)
    query = collection.aggregate(pipeline)
    result = 0
    for item in query:
        result = item['total']
    return result


def _build_pipeline(object_path: str, group: dict, unwind: bool = False, sort_key: Optional[SON] = None,
                    match: Optional[dict] = None) -> List[dict]:
    pipeline = []
    if unwind:
        pipeline.append({'$unwind': object_path})
    if match:
        pipeline.append({'$match': match})
    pipeline.append({'$group': group})
    if sort_key:
        pipeline.append({'$sort': sort_key})
    return pipeline
