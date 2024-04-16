import os

from models.invoice import Invoice 
import grpc


from payment_service_pb2 import (
     InvoiceRequest,
     UserInvoicesRequest
)


from payment_service_pb2_grpc import PaymentServiceStub

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


def getInvoice(invoiceId, token_info=None):

    if(token_info):
            userId = token_info['user_id']
    else:
        return 'Invalid user token', 403
    
    request = InvoiceRequest(invoiceId=invoiceId)
    response = client.GetInvoice(request)

    if (response.response_code == 0 and response.invoice.customer_id):
            
            parsed_invoice = __fromRPC(response.invoice)

            return parsed_invoice, 200
    elif response.response_code in [1,2,3]:
            return "No invoice found for the provided invoice ID", 404
    else:
        return 'Service is Unavailable', 500

def getInvoices(token_info=None):

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
