import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['inventory_service_pb2'] = MagicMock()
sys.modules['inventory_service_pb2_grpc'] = MagicMock()

from itemHandlerReview import *
batch_id = 123

class TestValidateBatch(unittest.TestCase):

    def test_validateBatch_batch_exists(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = 0
        self.assertTrue(validateBatch(batch_id))

    def test_validateBatch_batch_not_exists(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = 1
        self.assertFalse(validateBatch(batch_id))

    def test_getBatchScore(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().getBatchScoreService().score = 10
        self.assertEqual(getBatchScore(batch_id), 10)

    def test_getNvotos(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().getBatchUsersReviewService().n_users_review = 50
        self.assertEqual(getNvotos(batch_id), 50)

    def test_updateScore(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().updateScoreService().response_code = 8
        self.assertEqual(updateScore(batch_id, 8), 8)

if __name__ == '__main__':
    with open('./test-reports/reviewService_itemHandlerReview_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))
