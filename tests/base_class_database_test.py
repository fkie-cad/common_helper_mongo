import unittest
from pymongo import MongoClient


class MongoDbTest(unittest.TestCase):

    def setUp(self):
        self.mongo_client = MongoClient()
        self.db = self.mongo_client["common_code_test"]

    def tearDown(self):
        self.mongo_client.drop_database(self.db)
        self.mongo_client.close()

if __name__ == "__main__":
    unittest.main()
