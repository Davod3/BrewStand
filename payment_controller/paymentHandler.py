import connexion
import six

from models.invoice import Invoice 
from utils import util

from payment_service_pb2 import (
    InvoiceRequest,
    UserInvoicesRequest
)

from payment_service_pb2_grpc import PaymentStub

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50054")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentStub(payment_service_channel)

def billing_get_invoice(invoice_id):
    try:
        grpc_request = InvoiceRequest(invoiceId=invoice_id)
        response = client.GetInvoice(grpc_request)
        if(response.response_code == 0):
            return jsonify({"success": response.success, "invoice": response.invoice})
        elif(response.response_code == 1):
            return '', 404
        else:
            return '', 500

    except grpc.RpcError as e:
        return jsonify({"error": str(e)}), 500

def billing_get_invoices(): 
    try:
        grpc_request = UserInvoicesRequest()
        response = client.GetUserInvoices(grpc_request)
        if(response.response_code == 0):
            return jsonify({"invoices": response.invoices})
        elif(response.response_code == 1):
            return '', 404
        else:
            return '', 500

    except grpc.RpcError as e:
        return jsonify({"error": str(e)}), 500
