import unittest
from pymongo import MongoClient
import gridfs

from common_helper_mongo.gridfs import overwrite_file


class TestGridFS(unittest.TestCase):

    def setUp(self):
        self.mongo_client = MongoClient()
        self.db = self.mongo_client["common_code_test"]
        self.fs = gridfs.GridFS(self.db)

    def tearDown(self):
        self.mongo_client.drop_database(self.db)
        self.mongo_client.close()

    def testOverwriteFile(self):
        self.fs.put(b'original', filename="test_file")
        original_content = self.fs.find_one({'filename': "test_file"}).read()
        self.assertEqual(original_content, b'original', 'original content not correct')
        overwrite_file(self.fs, "test_file", b'changed')
        self.assertEqual(len(self.fs.list()), 1, "original file not deleted")
        changed_content = self.fs.find_one({'filename': "test_file"}).read()
        self.assertEqual(changed_content, b'changed', "content not correct")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
