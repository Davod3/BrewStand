import unittest
from unittest.mock import MagicMock, patch
import grpc
import sys
import xmlrunner

sys.modules['inventory_service_pb2'] = MagicMock()
sys.modules['order_service_pb2'] = MagicMock()
sys.modules['order_repository_pb2_grpc'] = MagicMock()
sys.modules['inventory_service_pb2_grpc'] = MagicMock()
sys.modules['order_repository_pb2'] = MagicMock()
sys.modules['models'] = MagicMock()
sys.modules['models.order'] = MagicMock()

from orderHandler import *


class TestOrderService(unittest.TestCase):

    def test_insertOrder_success(self):
        sys.modules['order_repository_pb2'].InsertOrderResponse().response_code = 0
        mock_context = MagicMock()
        request = MagicMock()
        response = insertOrder(request, mock_context)
        self.assertEqual(response.response_code, 0)

    def test_insertOrder_failure(self):
        sys.modules['order_repository_pb2'].InsertOrderResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = insertOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

    def test_getOrder_success(self):
        sys.modules['order_repository_pb2'].GetOrderResponse().response_code = 0
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrder(request, mock_context)
        self.assertEqual(response.response_code, 0)

    def test_getOrder_not_exist(self):
        sys.modules['order_repository_pb2'].GetOrderResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

    def test_getOrder_failure(self):
        sys.modules['order_repository_pb2'].GetOrderResponse().response_code = 2
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrder(request, mock_context)
        self.assertEqual(response.response_code, 2)

    def test_getOrders_success(self):
        sys.modules['order_repository_pb2'].GetOrdersResponse().response_code = 0
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrders(request, mock_context)
        self.assertEqual(response.response_code, 0)

    def test_getOrders_failure(self):
        sys.modules['order_repository_pb2'].GetOrdersResponse().response_code = 2
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrders(request, mock_context)
        self.assertEqual(response.response_code, 2)

    @patch('models.order.OrderRepoMongo.objects')
    def test_getOrders_order_invalid(self, mock_mongo):
        mock_mongo.return_value = []
        sys.modules['order_repository_pb2'].GetOrdersResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = getOrders(request, mock_context)
        self.assertEqual(response.response_code, 1)

if __name__ == '__main__':
    with open('./test-reports/order_repository_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))