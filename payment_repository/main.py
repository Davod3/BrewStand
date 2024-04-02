from concurrent import futures
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import payment_repository_pb2
import payment_repository_pb2_grpc

from models.invoice import Invoice
from mongoengine import *
from mongoengine.errors import NotUniqueError
import os

import paymentHandler

class PaymentRepositoryService(payment_repository_pb2_grpc.PaymentRepositoryServiceServicer):

    def StoreInvoice(self, request, context):
        try:
            invoice = Invoice.objects.create(
                price=request.invoice.price,
                order_id=request.invoice.orderID,
                customer_id=request.invoice.userId,
                fiscal_address=request.invoice.fiscalAddress,
                details=request.invoice.details
            )

            invoice_id = str(invoice.pk)
            invoice_data = paymentHandler.getInvoice(invoice_id)

            return payment_repository_pb2.StoreInvoiceResponse(
                response_code=0,
                invoiceId=invoice_id,
                invoice=invoice_data
            )
        except NotUniqueError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Invoice already exists')
            return payment_repository_pb2.StoreInvoiceResponse(response_code=1)

    
    def RetrieveInvoice(self, request, context):
        invoice = paymentHandler.getInvoice(request.invoiceId)
        if invoice:
            return payment_repository_pb2.RetrieveInvoiceResponse(
                response_code=0,
                invoiceId=invoice.invoice_id,
                invoice=invoice
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Invoice not found')
            return payment_repository_pb2.RetrieveInvoiceResponse(response_code=1)

    def GetUserInvoices(self, request, context):
        invoices = paymentHandler.getUserInvoices(request.userId)
        if invoices:
            return payment_repository_pb2.UserInvoicesResponse(invoices=invoices)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No invoices found for user')
            return payment_repository_pb2.UserInvoicesResponse(content = [])
    
def serve():
    __USER = os.getenv('MONGO_USER')
    __PASSWORD = os.getenv('MONGO_PASSWORD')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@cluster0.q350jt0.mongodb.net/db?retryWrites=true&w=majority&appName=Cluster0"
    connect(host=url)

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    payment_repository_pb2_grpc.add_PaymentRepositoryServiceServicer_to_server(
        PaymentRepositoryService(), server
    )

    server.add_insecure_port("[::]:50065")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
