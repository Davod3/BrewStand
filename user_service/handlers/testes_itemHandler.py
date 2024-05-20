import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['inventory_service_pb2'] = MagicMock()
sys.modules['inventory_service_pb2_grpc'] = MagicMock()

from itemHandler import *
batch_id = 123

class TestItemHandler(unittest.TestCase):

    def test_validate_item(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = True
        self.assertTrue(validateItem(batch_id))

    def test_validate_item_not_exists(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().validateItemService().response_code = False
        self.assertFalse(validateItem(batch_id))

    def test_get_batch_cost(self):
        sys.modules['inventory_service_pb2_grpc'].InventoryServiceStub().getBatchCostService().cost = 10.00
        self.assertEqual(getBatchCost(batch_id), 10.00)

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))