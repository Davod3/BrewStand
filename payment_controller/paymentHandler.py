import connexion

import os
import grpc

from payment_service_pb2 import (
    ProcessPaymentRequest,
    InvoiceRequest,
    UserInvoicesRequest
)

from payment_service_pb2_grpc import PaymentStub

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50054")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentStub(payment_service_channel)

def process_payment():
    if not connexion.request.is_json:
        return jsonify({"error": "Invalid request format"}), 400

    data = connexion.request.get_json()

    try:
        # Prepare the gRPC request
        grpc_request = ProcessPaymentRequest(
            userId=data['userId'],
            amount=data['amount'],
            currency=data['currency'],
            itemsName=data['itemsName'],
            fiscalAddress=data['fiscalAddress'],
            cardDetails=data['cardDetails']
        )

        # Call the gRPC service
        response = client.ProcessPayment(grpc_request)

        if(response.response_code==0):
            return '',200
        elif(response.response_code==1):
            return '',404
        elif(response.response_code==2 or response.response_code==3):
            return '', 400
        else:
            return '', 500
        
    except grpc.RpcError as e:
        return 'Invalid request body', 400

def get_invoice(userId, invoiceId):
    try:
        grpc_request = InvoiceRequest(userId=userId, invoiceId=invoiceId)
        response = client.GetInvoice(grpc_request)
        if(response.response_code == 0):
            return jsonify({"success": response.success, "invoice": response.invoice})
        elif(response.response_code == 1):
            return '', 404
        else:
            return '', 500

    except grpc.RpcError as e:
        return jsonify({"error": str(e)}), 500

def get_user_invoices(userId):
    try:
        grpc_request = UserInvoicesRequest(userId=userId)
        response = client.GetUserInvoices(grpc_request)
        if(response.response_code == 0):
            return jsonify({"invoices": response.invoices})
        elif(response.response_code == 1):
            return '', 404
        else:
            return '', 500

    except grpc.RpcError as e:
        return jsonify({"error": str(e)}), 500
