#!/usr/bin/python
"""
Add docstring here
"""
import os
import time
import unittest

import mock
from mock import patch
import mongomock


with patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient):
    os.environ['JEFF_MONGOALCHEMY_CONNECTION_STRING'] = ''
    os.environ['JEFF_MONGOALCHEMY_SERVER'] = ''
    os.environ['JEFF_MONGOALCHEMY_PORT'] = ''
    os.environ['JEFF_MONGOALCHEMY_DATABASE'] = ''

    from qube.src.models.jeff import jeff
    from qube.src.services.jeffservice import jeffService
    from qube.src.commons.context import AuthContext
    from qube.src.commons.error import ErrorCodes, jeffServiceError


class TestjeffService(unittest.TestCase):
    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setUp(self):
        context = AuthContext("23432523452345", "tenantname",
                              "987656789765670", "orgname", "1009009009988",
                              "username", False)
        self.jeffService = jeffService(context)
        self.jeff_api_model = self.createTestModelData()
        self.jeff_data = self.setupDatabaseRecords(self.jeff_api_model)
        self.jeff_someoneelses = \
            self.setupDatabaseRecords(self.jeff_api_model)
        self.jeff_someoneelses.tenantId = "123432523452345"
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            self.jeff_someoneelses.save()
        self.jeff_api_model_put_description \
            = self.createTestModelDataDescription()
        self.test_data_collection = [self.jeff_data]

    def tearDown(self):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            for item in self.test_data_collection:
                item.remove()
            self.jeff_data.remove()

    def createTestModelData(self):
        return {'name': 'test123123124'}

    def createTestModelDataDescription(self):
        return {'description': 'test123123124'}

    @mock.patch('pymongo.mongo_client.MongoClient', new=mongomock.MongoClient)
    def setupDatabaseRecords(self, jeff_api_model):
        with patch('mongomock.write_concern.WriteConcern.__init__',
                   return_value=None):
            jeff_data = jeff(name='test_record')
            for key in jeff_api_model:
                jeff_data.__setattr__(key, jeff_api_model[key])

            jeff_data.description = 'my short description'
            jeff_data.tenantId = "23432523452345"
            jeff_data.orgId = "987656789765670"
            jeff_data.createdBy = "1009009009988"
            jeff_data.modifiedBy = "1009009009988"
            jeff_data.createDate = str(int(time.time()))
            jeff_data.modifiedDate = str(int(time.time()))
            jeff_data.save()
            return jeff_data

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_post_jeff(self, *args, **kwargs):
        result = self.jeffService.save(self.jeff_api_model)
        self.assertTrue(result['id'] is not None)
        self.assertTrue(result['name'] == self.jeff_api_model['name'])
        jeff.query.get(result['id']).remove()

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_jeff(self, *args, **kwargs):
        self.jeff_api_model['name'] = 'modified for put'
        id_to_find = str(self.jeff_data.mongo_id)
        result = self.jeffService.update(
            self.jeff_api_model, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['name'] == self.jeff_api_model['name'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_put_jeff_description(self, *args, **kwargs):
        self.jeff_api_model_put_description['description'] =\
            'modified for put'
        id_to_find = str(self.jeff_data.mongo_id)
        result = self.jeffService.update(
            self.jeff_api_model_put_description, id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))
        self.assertTrue(result['description'] ==
                        self.jeff_api_model_put_description['description'])

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff_item(self, *args, **kwargs):
        id_to_find = str(self.jeff_data.mongo_id)
        result = self.jeffService.find_by_id(id_to_find)
        self.assertTrue(result['id'] == str(id_to_find))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff_item_invalid(self, *args, **kwargs):
        id_to_find = '123notexist'
        with self.assertRaises(jeffServiceError):
            self.jeffService.find_by_id(id_to_find)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_get_jeff_list(self, *args, **kwargs):
        result_collection = self.jeffService.get_all()
        self.assertTrue(len(result_collection) == 1,
                        "Expected result 1 but got {} ".
                        format(str(len(result_collection))))
        self.assertTrue(result_collection[0]['id'] ==
                        str(self.jeff_data.mongo_id))

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_not_system_user(self, *args, **kwargs):
        id_to_delete = str(self.jeff_data.mongo_id)
        with self.assertRaises(jeffServiceError) as ex:
            self.jeffService.delete(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_ALLOWED)

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_by_system_user(self, *args, **kwargs):
        id_to_delete = str(self.jeff_data.mongo_id)
        self.jeffService.auth_context.is_system_user = True
        self.jeffService.delete(id_to_delete)
        with self.assertRaises(jeffServiceError) as ex:
            self.jeffService.find_by_id(id_to_delete)
        self.assertEquals(ex.exception.errors, ErrorCodes.NOT_FOUND)
        self.jeffService.auth_context.is_system_user = False

    @patch('mongomock.write_concern.WriteConcern.__init__', return_value=None)
    def test_delete_toolchain_item_someoneelse(self, *args, **kwargs):
        id_to_delete = str(self.jeff_someoneelses.mongo_id)
        with self.assertRaises(jeffServiceError):
            self.jeffService.delete(id_to_delete)
