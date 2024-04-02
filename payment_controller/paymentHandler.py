import os

from models.invoice import Invoice 
import grpc


import payment_service_pb2


from payment_service_pb2_grpc import PaymentServiceStub

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50055")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentServiceStub(payment_service_channel)

def getInvoice(invoice_id):
    request = payment_service_pb2.InvoiceRequest(invoice_id=invoice_id)
    response = client.GetInvoice(request)

    if response.response_code == 0:
        return '', 200
    elif response.response_code == 1:
        return '', 404
    elif response.response_code in [2, 3]:
        return '', 400
    else:
        return '', 500

def getInvoices(userId): 
    request = payment_service_pb2.UserInvoicesRequest(userId=userId) 
    response = client.GetAllUserInvoices(request)  
    
    if response:
        if response.invoices:
            return response.invoices, 200
        else:
            return {"message": "No invoices found for the provided user ID"}, 404
    else:
        return {"error": "No response from server"}, 500
