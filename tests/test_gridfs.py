import unittest
import gridfs

from common_helper_mongo.gridfs import overwrite_file
from tests.base_class_database_test import MongoDbTest


class TestGridFS(MongoDbTest):

    def setUp(self):
        super().setUp()
        self.fs = gridfs.GridFS(self.db)

    def testOverwriteFile(self):
        self.fs.put(b'original', filename="test_file")
        original_content = self.fs.find_one({'filename': "test_file"}).read()
        self.assertEqual(original_content, b'original', 'original content not correct')
        overwrite_file(self.fs, "test_file", b'changed')
        self.assertEqual(len(self.fs.list()), 1, "original file not deleted")
        changed_content = self.fs.find_one({'filename': "test_file"}).read()
        self.assertEqual(changed_content, b'changed', "content not correct")


if __name__ == "__main__":
    unittest.main()
