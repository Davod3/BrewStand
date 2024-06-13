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

from orderHandler import *


class TestOrderService(unittest.TestCase):

    def test_getOrder_success(self):
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub().GetOrder().order = MagicMock()
        sys.modules['order_service_pb2'].GetOrderServiceResponse().response_code = 0
        sys.modules['order_service_pb2'].GetOrderServiceResponse().order = "123"
        mock_context = MagicMock()
        request = MagicMock(order_id="123")
        response = getOrder(request, mock_context)
        self.assertEqual(response.response_code, 0)
        self.assertEqual(response.order, "123")

    def test_getOrder_failure(self):
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub().GetOrder().order = MagicMock()
        sys.modules['order_service_pb2'].GetOrderServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock(order_id="123")
        response = getOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

    def test_getOrders_success(self):
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub().GetOrders().orders = MagicMock()
        sys.modules['order_service_pb2'].GetOrdersServiceResponse().response_code = 0
        sys.modules['order_service_pb2'].GetOrdersServiceResponse().orders = ["123", "321"]
        mock_context = MagicMock()
        request = MagicMock(user_id="1")
        response = getOrders(request, mock_context)
        self.assertEqual(response.response_code, 0)
        self.assertEqual(response.orders, ["123", "321"])

    def test_getOrders_failure(self):
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub().GetOrders().orders = MagicMock()
        sys.modules['order_service_pb2'].GetOrdersServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock(user_id="1")
        response = getOrders(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('orderHandler.validateOrderItems')
    def test_createOrder_order_invalid(self, mock_order):
        mock_order.return_value = False
        sys.modules['order_service_pb2'].CreateOrderServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = createOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('orderHandler.validateOrderItems')
    @patch('orderHandler.updateVolumeForItems')
    def test_createOrder_update_invalid(self, mock_order_validate, mock_order):
        mock_order_validate.return_value = False
        mock_order.return_value = True
        sys.modules['order_service_pb2'].CreateOrderServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = createOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

    @patch('orderHandler.validateOrderItems')
    @patch('orderHandler.updateVolumeForItems')
    def test_createOrder_success(self, mock_order_validate, mock_order):
        mock_order_validate.return_value = True
        mock_order.return_value = True
        sys.modules['order_repository_pb2'].ItemRepo.itemID = 123
        sys.modules['order_repository_pb2'].ItemRepo.volume = 2
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub.InsertOrder.response_code = 0
        sys.modules['order_service_pb2'].CreateOrderServiceResponse().response_code = 0
        mock_context = MagicMock()
        request = MagicMock()
        response = createOrder(request, mock_context)
        self.assertEqual(response.response_code, 0)

    @patch('orderHandler.validateOrderItems')
    @patch('orderHandler.updateVolumeForItems')
    def test_createOrder_failure(self, mock_order_validate, mock_order):
        mock_order_validate.return_value = True
        mock_order.return_value = True
        sys.modules['order_repository_pb2'].ItemRepo.itemID = 123
        sys.modules['order_repository_pb2'].ItemRepo.volume = 2
        sys.modules['order_repository_pb2_grpc'].OrderRepositoryStub.InsertOrder.response_code = 1
        sys.modules['order_service_pb2'].CreateOrderServiceResponse().response_code = 1
        mock_context = MagicMock()
        request = MagicMock()
        response = createOrder(request, mock_context)
        self.assertEqual(response.response_code, 1)

if __name__ == '__main__':
    with open('./test-reports/order_service_tests.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))