import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner

sys.modules['payment_repository_pb2'] = MagicMock()
sys.modules['payment_repository_pb2_grpc'] = MagicMock()

from invoiceHandler import *

class TestInvoiceHandler(unittest.TestCase):

    def test_getInvoice(self):
        sys.modules['payment_repository_pb2_grpc'].PaymentRepositoryServiceStub().RetrieveInvoice().invoiceId = "123"
        self.assertEqual(getInvoice(123).invoiceId, "123")

    def test_getUserInvoices(self):
        mock_invoice = MagicMock()
        mock_invoice.invoice_id = "123"
        mock_invoice.price = 100.0
        mock_invoice.order_id = "456"
        mock_invoice.customer_id = "789"
        mock_invoice.fiscal_address = "Test Address"
        mock_invoice.details = "Test Details"
        
        mock_response = MagicMock()
        mock_response.invoices = [mock_invoice]
        sys.modules['payment_repository_pb2_grpc'].PaymentRepositoryServiceStub().GetUserInvoices().invoices = mock_response
        
        result = getUserInvoices(789).invoices
        self.assertEqual(len(result), 1) 
        self.assertEqual(result[0].invoice_id, "123")
        self.assertEqual(result[0].price, 100.0)
        self.assertEqual(result[0].order_id, "456")
        self.assertEqual(result[0].customer_id, "789")
        self.assertEqual(result[0].fiscal_address, "Test Address")
        self.assertEqual(result[0].details, "Test Details")

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
