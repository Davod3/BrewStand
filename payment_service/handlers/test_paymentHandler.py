import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['payment_service_pb2'] = MagicMock()
sys.modules['order_service_pb2'] = MagicMock()
sys.modules['order_service_pb2_grpc'] = MagicMock()
sys.modules['payment_repository_pb2_grpc'] = MagicMock()
sys.modules['payment_repository_pb2'] = MagicMock()

from paymentHandler import *

class TestInvoiceHandler(unittest.TestCase):

    def test_validate_card_details(self):
        card_details = ""
        self.assertEqual(validate_card_details(card_details), (True, ""))

    def test_validate_card_number(self):
        card_number = ""
        self.assertEqual(validate_card_number(card_number), True)

    def test_validate_card_expiry(self):
        expiry_date = ""
        self.assertEqual(validate_card_expiry(expiry_date), True)

    def test_validate_cvc(self):
        cvc = ""
        self.assertEqual(validate_cvc(cvc), True)

    def test_contact_payment_gateway(self):
        user_id = ""
        amount = ""
        currency = ""
        card_details = ""

        response = contact_payment_gateway(user_id, amount, currency, card_details)

        self.assertTrue(response['success'], True)
        self.assertEqual(response['transaction_id'], 'txn12345')
        self.assertEqual(response['message'], 'Payment processed successfully')

    @patch('paymentHandler.validate_card_details')
    @patch('paymentHandler.contact_payment_gateway')
    def test_validate_payment(self, mock_contact_payment_gateway, mock_validate_card_details):
        user_id = ""
        amount = ""
        currency = ""
        items = ""
        fiscal_address = ""
        card_details = MagicMock()

        mock_validate_card_details.return_value = (True, "")
        mock_contact_payment_gateway.return_value = {
            'success': True,
            'transaction_id': 'txn12345',
            'message': 'Payment processed successfully'
        }

        card_last_four, error_message = validate_payment(
            user_id, amount, currency, items, fiscal_address, card_details
        )

        self.assertEqual(card_last_four, card_details.cardNumber[-4:])
        self.assertIsNone(error_message)

    @patch('paymentHandler.validate_payment')
    @patch('paymentHandler.client')
    def test_process_payment_success(self, mock_client, mock_validate_payment):
        user_id = ""
        amount = ""
        currency = ""
        items = [{"batch_id": 123, "volume": 2}]
        fiscal_address = ""
        card_details = MagicMock()

        mock_validate_payment.return_value = (card_details.cardNumber[-4:], None)

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().itemID = 123
        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().volume = 2

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().CreateOrderServiceRequest().response_code = 0

        sys.modules['order_service_pb2_grpc'].OrderStub().CreateOrder().response_code = 0

        mock_invoice = MagicMock()
        mock_invoice.invoice_id = "123"
        mock_invoice.price = 100.0
        mock_invoice.order_id = "456"
        mock_invoice.customer_id = "789"
        mock_invoice.fiscal_address = "Test Address"
        mock_invoice.details = "Test Details"
        
        mock_response = MagicMock()
        mock_response.invoice = [mock_invoice]

        mock_client.StoreInvoice().response_code = 0
        mock_client.StoreInvoice().invoiceId = "123"
        mock_client.StoreInvoice().invoice = [mock_invoice]

        sys.modules['payment_service_pb2'].ProcessPaymentResponse().response_code = 0
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoiceId = "123"
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoice = [mock_invoice]

        result = process_payment(
            user_id, amount, currency, fiscal_address, items, card_details
        )

        self.assertEqual(result.response_code, 0)
        self.assertEqual(result.invoiceId, "123")

        self.assertEqual(len(result.invoice), 1)  # Assuming only one invoice is returned
        self.assertEqual(result.invoice[0].invoice_id, "123")
        self.assertEqual(result.invoice[0].price, 100.0)
        self.assertEqual(result.invoice[0].order_id, "456")
        self.assertEqual(result.invoice[0].customer_id, "789")
        self.assertEqual(result.invoice[0].fiscal_address, "Test Address")
        self.assertEqual(result.invoice[0].details, "Test Details")


    @patch('paymentHandler.validate_payment')
    @patch('paymentHandler.client')
    def test_process_payment_error_order_response(self, mock_client, mock_validate_payment):
        user_id = ""
        amount = ""
        currency = ""
        items = [{"batch_id": 123, "volume": 2}]
        fiscal_address = ""
        card_details = MagicMock()

        mock_validate_payment.return_value = (card_details.cardNumber[-4:], None)

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().itemID = 123
        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().volume = 2

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().CreateOrderServiceRequest().response_code = 1

        sys.modules['order_service_pb2_grpc'].OrderStub().CreateOrder().response_code = 1

        sys.modules['payment_service_pb2'].ProcessPaymentResponse().response_code = 2
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoiceId = ""
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoice = None

        result = process_payment(
            user_id, amount, currency, fiscal_address, items, card_details
        )

        self.assertEqual(result.response_code, 2)
        self.assertEqual(result.invoiceId, "")
        self.assertIsNone(result.invoice)

    @patch('paymentHandler.validate_payment')
    @patch('paymentHandler.client')
    def test_process_payment_error_store_invoice_response(self, mock_client, mock_validate_payment):
        user_id = ""
        amount = ""
        currency = ""
        items = [{"batch_id": 123, "volume": 2}]
        fiscal_address = ""
        card_details = MagicMock()

        mock_validate_payment.return_value = (card_details.cardNumber[-4:], None)

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().itemID = 123
        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().ItemDetails().volume = 2

        sys.modules['order_service_pb2'].PaymentRepositoryServiceStub().CreateOrderServiceRequest().response_code = 0

        sys.modules['order_service_pb2_grpc'].OrderStub().CreateOrder().response_code = 0

        mock_invoice = MagicMock()
        mock_invoice.invoice_id = "123"
        mock_invoice.price = 100.0
        mock_invoice.order_id = "456"
        mock_invoice.customer_id = "789"
        mock_invoice.fiscal_address = "Test Address"
        mock_invoice.details = "Test Details"
        
        mock_response = MagicMock()
        mock_response.invoice = [mock_invoice]

        mock_client.StoreInvoice().response_code = 1

        sys.modules['payment_service_pb2'].ProcessPaymentResponse().response_code = 2
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoiceId = ""
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoice = None

        result = process_payment(
            user_id, amount, currency, fiscal_address, items, card_details
        )

        self.assertEqual(result.response_code, 2)
        self.assertEqual(result.invoiceId, "")
        self.assertIsNone(result.invoice)

    @patch('paymentHandler.validate_payment')
    @patch('paymentHandler.client')
    def test_process_payment_error_card_last_four(self, mock_client, mock_validate_payment):
        user_id = ""
        amount = ""
        currency = ""
        items = [{"batch_id": 123, "volume": 2}]
        fiscal_address = ""
        card_details = MagicMock()

        mock_validate_payment.return_value = (None, "Error")

        sys.modules['payment_service_pb2'].ProcessPaymentResponse().response_code = 2
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoiceId = ""
        sys.modules['payment_service_pb2'].ProcessPaymentResponse().invoice = None

        result = process_payment(
            user_id, amount, currency, fiscal_address, items, card_details
        )

        self.assertEqual(result.response_code, 2)
        self.assertEqual(result.invoiceId, "")
        self.assertIsNone(result.invoice)


if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
