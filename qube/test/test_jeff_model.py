#!/usr/bin/python
"""
Add docstring here
"""
import time
import unittest

import mock

from mock import patch
import mongomock


class TestjeffModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("before class")

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def test_create_jeff_model(self):
        from qube.src.models.jeff import jeff
        jeff_data = jeff(name='testname')
        jeff_data.tenantId = "23432523452345"
        jeff_data.orgId = "987656789765670"
        jeff_data.createdBy = "1009009009988"
        jeff_data.modifiedBy = "1009009009988"
        jeff_data.createDate = str(int(time.time()))
        jeff_data.modifiedDate = str(int(time.time()))
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            jeff_data.save()
            self.assertIsNotNone(jeff_data.mongo_id)
            jeff_data.remove()

    @classmethod
    def tearDownClass(cls):
        print("After class")


if __name__ == '__main__':
    unittest.main()
