import os

from models.invoice import Invoice 
import grpc


from payment_service_pb2 import (
     InvoiceRequest,
     UserInvoicesRequest
)


from payment_service_pb2_grpc import PaymentServiceStub

from prometheus_client import Counter, Summary

total_received_requests_metric = Counter('payment_total_received_requests', 'Total number of requests received by the Payment API')

duration_get_invoice = Summary('duration_get_invoice_seconds', 'Average time in seconds it takes for a user to get an invoice')
duration_get_invoices = Summary('duration_get_invoices_seconds', 'Average time in seconds it takes for a user to get invoices')

failures_get_invoice = Counter('failures_get_invoice', 'Number of failures when a user gets an invoice')
failures_get_invoices = Counter('failures_get_invoices', 'Number of failures when a user gets invoices')

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50055")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentServiceStub(payment_service_channel)

def __fromRPC(invoice):

    return Invoice.from_dict({
         'invoiceID' : invoice.invoice_id,
         'price' : invoice.price,
         'orderID' : invoice.order_id,
         'customerID' : invoice.customer_id,
         'fiscalAddress' : invoice.fiscal_address,
         'details' : invoice.details
    })


@duration_get_invoice.time()
@failures_get_invoice.count_exceptions()
def getInvoice(invoiceId, token_info=None):

    total_received_requests_metric.inc()

    if(token_info):
            userId = token_info['user_id']
    else:
        return 'Invalid user token', 403
    
    request = InvoiceRequest(invoiceId=invoiceId)
    response = client.GetInvoice(request)

    if (response.response_code == 0 and response.invoice.customer_id == userId):
            
            parsed_invoice = __fromRPC(response.invoice)

            return parsed_invoice, 200
    elif response.response_code in [1,2,3]:
            return "No invoice found for the provided invoice ID", 404
    else:
        return 'Service is Unavailable', 500

@duration_get_invoices.time()
@failures_get_invoices.count_exceptions()
def getInvoices(token_info=None):

    total_received_requests_metric.inc()

    if(token_info):
            userId = token_info['user_id']
    else:
        return 'Invalid user token', 403

    request = UserInvoicesRequest(userId=userId) 
    response = client.GetAllUserInvoices(request)  

    if response:    
        
        invoices = list()

        for invoice in response.invoices:
             
             parsed_invoice = __fromRPC(invoice)
             invoices.append(parsed_invoice)

        return invoices, 200
    else:
        return "Service is Unavailable", 500
