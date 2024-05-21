import unittest
from unittest.mock import MagicMock, patch
import sys
import xmlrunner
sys.modules['payment_repository_pb2'] = MagicMock()
sys.modules['models.invoice'] = MagicMock()

from paymentHandler import *

class TestPaymentHandler(unittest.TestCase):

    #@patch('paymentHandler.Invoice.objects.with_id')
    def test_getInvoice_invoice_found(self):

        mock_invoice = MagicMock()
        mock_invoice.invoice_id = '123'
        mock_invoice.price = 100
        mock_invoice.order_id = 'order_123'
        mock_invoice.customer_id = 'customer_123'
        mock_invoice.fiscal_address = '123 Main St'
        mock_invoice.details = 'Details for invoice 123'
        
        sys.modules['payment_repository_pb2'].InvoiceData().invoice_id = '123'
        sys.modules['payment_repository_pb2'].InvoiceData().price = 100
        sys.modules['payment_repository_pb2'].InvoiceData().order_id = 'order_123'
        sys.modules['payment_repository_pb2'].InvoiceData().customer_id = 'customer_123'
        sys.modules['payment_repository_pb2'].InvoiceData().fiscal_address = '123 Main St'
        sys.modules['payment_repository_pb2'].InvoiceData().details = 'Details for invoice 123'
        
        result = getInvoice('invoice123')

        self.assertEqual(result.invoice_id, '123')
        self.assertEqual(result.price, 100)
        self.assertEqual(result.order_id, 'order_123')
        self.assertEqual(result.customer_id, 'customer_123')
        self.assertEqual(result.fiscal_address, '123 Main St')
        self.assertEqual(result.details, 'Details for invoice 123')


    @patch('paymentHandler.Invoice.objects')
    def test_getInvoice_not_found(self, mock_objects):
        mock_objects.return_value = None

        result = getInvoices('user123')

        self.assertEqual(result, [])

    # def test_convertRPC(self):
    #     mock_invoice = MagicMock()
    #     mock_invoice.invoice_id = '123'
    #     mock_invoice.price = 100
    #     mock_invoice.order_id = 'order_123'
    #     mock_invoice.customer_id = 'customer_123'
    #     mock_invoice.fiscal_address = '123 Main St'
    #     mock_invoice.details = 'Details for invoice 123'
        
    #     sys.modules['payment_repository_pb2'].InvoiceData().invoice_id = '123'
    #     sys.modules['payment_repository_pb2'].InvoiceData().price = 100
    #     sys.modules['payment_repository_pb2'].InvoiceData().order_id = 'order_123'
    #     sys.modules['payment_repository_pb2'].InvoiceData().customer_id = 'customer_123'
    #     sys.modules['payment_repository_pb2'].InvoiceData().fiscal_address = '123 Main St'
    #     sys.modules['payment_repository_pb2'].InvoiceData().details = 'Details for invoice 123'
        
    #     result = convertToRPC(mock_invoice)

    #     self.assertEqual(result.invoice_id, '123')
    #     self.assertEqual(result.price, 100)
    #     self.assertEqual(result.order_id, 'order_123')
    #     self.assertEqual(result.customer_id, 'customer_123')
    #     self.assertEqual(result.fiscal_address, '123 Main St')
    #     self.assertEqual(result.details, 'Details for invoice 123')

    @patch('paymentHandler.Invoice.objects')
    def test_getInvoices_with_invoices(self, mock_objects):
        mock_invoice1 = MagicMock()
        mock_invoice2 = MagicMock()

        mock_objects.return_value = [mock_invoice1, mock_invoice2]

        result = getInvoices('user123')
        sys.modules['payment_repository_pb2'].InvoiceData().invoice_id='123'
        sys.modules['payment_repository_pb2'].InvoiceData().invoice_id1='456'
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].invoice_id, '123')
        self.assertEqual(result[1].invoice_id1, '456')


    @patch('paymentHandler.Invoice.objects')
    def test_getInvoices_no_invoices(self, mock_objects):
        mock_objects.return_value = []

        result = getInvoices('user123')

        self.assertEqual(result, [])

if __name__ == '__main__':
    with open('./test-reports/payment_paymentHandler.xml', 'wb') as output:
        unittest.main(testRunner=xmlrunner.XMLTestRunner(output=output))
