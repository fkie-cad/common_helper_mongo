import unittest
from pymongo import MongoClient


class MongoDbTest(unittest.TestCase):

    def setUp(self):
        self.mongo_client = MongoClient()
        self.db = self.mongo_client["common_code_test"]
        self.test_collection = self.db.test_data

    def tearDown(self):
        self.mongo_client.drop_database(self.db)
        self.mongo_client.close()

    def add_simple_test_data(self):
        for i in range(10):
            self.test_collection.insert_one({"test_int": i, "test_txt": "item {}".format(i)})
        self.test_collection.insert_one({"test_txt": "item 1"})

    def add_list_test_data(self):
        self.test_collection.insert_one({"test_list": ["a", "b", "c"]})
        self.test_collection.insert_one({"test_list": ["c", "d"]})

if __name__ == "__main__":
    unittest.main()
