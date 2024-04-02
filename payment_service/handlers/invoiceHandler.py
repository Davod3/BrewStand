# handlers/invoiceHandler.py

import os
import grpc

from payment_repository_pb2 import RetrieveInvoiceRequest, GetUserInvoicesRequest
from payment_repository_pb2_grpc import PaymentRepositoryServiceStub

payment_repository_host = os.getenv("PAYMENT_REPOSITORY_HOST", "localhost")
payment_repository_port = os.getenv("PAYMENT_REPOSITORY_PORT", "50064")
payment_repository_channel = grpc.insecure_channel(f"{payment_repository_host}:{payment_repository_port}")

client = PaymentRepositoryServiceStub(payment_repository_channel)

def getInvoice(invoiceId):
    try:
        retrieve_response = client.RetrieveInvoice(
            RetrieveInvoiceRequest(invoiceId=invoiceId)
        )
        return retrieve_response
        
    except grpc.RpcError as e:
        return []

def getUserInvoices(userId):
    try:
        user_invoices_response = client.GetUserInvoices(
            GetUserInvoicesRequest(userId=userId)
        )

        return user_invoices_response

    except grpc.RpcError as e:
        return []