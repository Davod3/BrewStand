import os

from models.invoice import Invoice 
import grpc


from payment_service_pb2 import (
    InvoiceRequest,
    UserInvoicesRequest
)

from payment_service_pb2_grpc import PaymentServiceStub

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50054")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentServiceStub(payment_service_channel)

def getInvoice(invoice_id):
    request = InvoiceRequest(invoice_id=invoice_id)
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
    request = UserInvoicesRequest(userId=userId)
    response = client.GetAllUserInvoices(request)

    if response.response_code == 0:
        return response.invoices, 200
    elif response.response_code == 1:
        return {"error": "No invoices found for the provided user ID"}, 404
    elif response.response_code in [2, 3]:
        return {"error": "Invalid request or server error"}, 400
    else:
        return {"error": "Internal server error"}, 500

