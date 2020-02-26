from common_helper_mongo.aggregate import (
    get_all_value_combinations_of_fields, get_field_average, get_field_sum, get_list_of_all_values,
    get_objects_and_count_of_occurrence
)
from tests.base_class_database_test import MongoDbTest


class TestAggregate(MongoDbTest):

    def test_get_list_of_all_values(self):
        self.add_simple_test_data()
        result = get_list_of_all_values(self.test_collection, "$test_txt", unwind=False, match=None)
        self.assertIsInstance(result, list, "result not a list")
        self.assertEqual(len(result), 10, "number of results not correct")
        self.assertEqual(result[0], "item 0", "first item not correct")

    def test_get_list_of_all_values_match(self):
        self.add_simple_test_data()
        result = get_list_of_all_values(self.test_collection, "$test_txt", unwind=False, match={"test_int": {"$lt": 5}})
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], "item 0")

    def test_get_list_of_all_values_unwind(self):
        self.add_list_test_data()
        result = get_list_of_all_values(self.test_collection, "$test_list", unwind=True, match=None)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], "a")

    def test_get_all_value_combinations_of_fields(self):
        self.test_collection.insert_many([
            {"test_list": ["a", "b"], "test_value": 1},
            {"test_list": ["c", "d"], "test_value": 2},
            {"test_list": ["a", "d"], "test_value": 1}
        ])
        result = get_all_value_combinations_of_fields(self.test_collection, "$test_list", "$test_value", unwind=True)
        assert result == {'a': [1], 'b': [1], 'c': [2], 'd': [1, 2]}

    def test_get_all_value_combinations_of_fields_id(self):
        self.add_list_test_data()
        result = get_all_value_combinations_of_fields(self.test_collection, "$test_list", "$_id", unwind=True)
        self.assertIsInstance(result, dict, "result should be a dict")
        self.assertEqual(len(result.keys()), 4, "number of results not correct")
        self.assertEqual(len(result['c']), 2, "c should have two related object ids")
        self.assertEqual(len(result['a']), 1, "a should have one related object id")

    def test_get_objects_and_count_of_occurrence(self):
        self.add_simple_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_txt", unwind=False, match=None)
        self.assertEqual(len(result), 10, "number of results not correct")
        self.assertEqual(result[0]['_id'], "item 1", "should be the fist element because it has two occurrences")
        self.assertEqual(result[0]['count'], 2)

    def test_get_objects_and_count_unwind(self):
        self.add_list_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_list", unwind=True, match=None)
        self.assertEqual(len(result), 4, "number of results not correct")
        self.assertEqual(result[0]['_id'], "c", "should be the first element because it has two occurrences")
        self.assertEqual(result[0]['count'], 2)

    def test_get_objects_and_count_match(self):
        self.add_simple_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_txt", unwind=False, match={"test_int": 0})
        self.assertEqual(len(result), 1, "number of results not correct")
        self.assertEqual(result[0]['_id'], "item 0")

    def test_get_field_sum(self):
        self.add_simple_test_data()
        result = get_field_sum(self.test_collection, "$test_int")
        self.assertEqual(result, 45)

    def test_get_field_avg(self):
        self.add_simple_test_data()
        result = get_field_average(self.test_collection, "$test_int")
        self.assertEqual(result, 4.5)

    def test_get_field_sum_match(self):
        self.add_simple_test_data()
        result = get_field_sum(self.test_collection, "$test_int", match={"test_int": {"$lt": 5}})
        self.assertEqual(result, 10)

    def test_get_field_execute_operation_empty(self):
        result = get_field_sum(self.test_collection, "$test_int")
        self.assertEqual(result, 0)
