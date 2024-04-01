import connexion
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
    if connexion.request.is_json:
        invoice = Invoice.from_dict(connexion.request.get_json())

        request = InvoiceRequest(invoice_id = invoice.invoice_id)
        response = client.GetInvoice(request)

        if(response.response_code==0):
            return '',200
        elif(response.response_code==1):
            return '',404
        elif(response.response_code==2 or response.response_code==3):
            return '', 400
        else:
            return '', 500

    else:
        return 'Invalid request body', 400
   
def getInvoices(): 
    if connexion.request.is_json:

        request = UserInvoicesRequest(user_id = user_id)
        response = client.GetAllInvoices(request)

        if(response.response_code==0):
            return '',200
        elif(response.response_code==1):
            return '',404
        elif(response.response_code==2 or response.response_code==3):
            return '', 400
        else:
            return '', 500

    else:
        return 'Invalid request body', 400