import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['payment_service_pb2'] = MagicMock()
sys.modules['payment_service_pb2_grpc'] = MagicMock()
sys.modules['handlers'] = MagicMock()
sys.modules['handlers.userHandler'] = MagicMock()
sys.modules['UserHandler'] = MagicMock()

from billingHandler import *
batch_id = 123

class TestItemHandler(unittest.TestCase):

    @patch('billingHandler.UserHandler.getCartContent')
    def test_user_not_found(self, mock_get_cart_content):
        mock_get_cart_content.return_value = (1, None, None)

        result = initiatePayment('invalid_user_id', 'card_number', 'card_expiry', 'card_cvc')

        self.assertEqual(result[0], 1)

    @patch('billingHandler.UserHandler.getCartContent')
    def test_empty_cart(self, mock_get_cart_content):
        mock_get_cart_content.return_value = (0, [], 0)

        result = initiatePayment('user_id', 'card_number', 'card_expiry', 'card_cvc')

        self.assertEqual(result[0], 2)

    @patch('billingHandler.UserHandler.getCartContent')
    @patch('billingHandler.UserHandler.getUserByID')
    @patch('billingHandler.UserHandler.deleteFromCart')
    @patch('billingHandler.client.ProcessPayment')
    def test_invalid_order(self, mock_process_payment, mock_delete_from_cart, mock_get_user_by_id, mock_get_cart_content):
        mock_cart_item = MagicMock(batch_id=123, volume=2)
        mock_get_cart_content.return_value = (0, [mock_cart_item], 10)
        mock_get_user_by_id.return_value = MagicMock(address='Some Address')
        mock_response = MagicMock(response_code=3)
        mock_process_payment.return_value = mock_response

        result = initiatePayment('user_id', 'card_number', 'card_expiry', 'card_cvc')

        self.assertEqual(result[0], 3)
        mock_delete_from_cart.assert_not_called()

    @patch('billingHandler.UserHandler.getCartContent')
    @patch('billingHandler.UserHandler.getUserByID')
    @patch('billingHandler.UserHandler.deleteFromCart')
    @patch('billingHandler.client.ProcessPayment')
    def test_successful_payment(self, mock_process_payment, mock_delete_from_cart, mock_get_user_by_id, mock_get_cart_content):
        mock_cart_item = MagicMock(batch_id=123, volume=2)
        mock_get_cart_content.return_value = (0, [mock_cart_item], 10)
        mock_get_user_by_id.return_value = MagicMock(address='Some Address') 
        mock_response = MagicMock(response_code=0, invoiceId='INV123', invoice=MagicMock(price=10, order_id='ORDER123', customer_id='CUST123', fiscal_address='Some Address', details='Some Details'))  # Mocking payment response
        mock_process_payment.return_value = mock_response

        result = initiatePayment('user_id', 'card_number', 'card_expiry', 'card_cvc')

        self.assertEqual(result[0], 0)
        self.assertEqual(result[1], 'INV123') 
        self.assertEqual(result[2], 10)
        self.assertEqual(result[3], 'ORDER123')
        self.assertEqual(result[4], 'CUST123')
        self.assertEqual(result[5], 'Some Address')
        self.assertEqual(result[6], 'Some Details')
        mock_delete_from_cart.assert_called_once_with(user_id='user_id')


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))