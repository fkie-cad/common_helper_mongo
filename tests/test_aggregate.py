from common_helper_mongo.aggregate import get_objects_and_count_of_occurrence,\
    get_field_sum, get_field_average, get_list_of_all_values
import unittest
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

    def test_get_objects_and_count_of_occurence(self):
        self.add_simple_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_txt", unwind=False, match=None)
        self.assertEqual(len(result), 10, "number of results not correct")
        self.assertEqual(result[0]['_id'], "item 1", "should be the fist element because it has two ocurrences")
        self.assertEqual(result[0]['count'], 2)

    def test_get_objects_and_count_unwind(self):
        self.add_list_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_list", unwind=True, match=None)
        self.assertEqual(len(result), 4, "number of results not correct")
        self.assertEqual(result[0]['_id'], "c", "should be the first element because it has two ocurrences")
        self.assertEqual(result[0]['count'], 2)

    def test_get_objects_and_count_match(self):
        self.add_simple_test_data()
        result = get_objects_and_count_of_occurrence(self.test_collection, "$test_txt", unwind="False", match={"test_int": 0})
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


if __name__ == "__main__":
    unittest.main()
