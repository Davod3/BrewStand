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

# Assuming paymentHandler is a module you have that contains the logic for handling invoices.
import paymentHandler

class PaymentRepositoryService(payment_repository_pb2_grpc.PaymentRepositoryServiceServicer):

    def StoreInvoice(self, request, context):
        try:
            invoice = Invoice(
                price=request.invoice.price,
                orderID=request.invoice.orderID,
                userId=request.invoice.userId,
                fiscalAddress=request.invoice.fiscalAddress,
                cardLastFour=request.invoice.cardLastFour,
                items_name=request.invoice.items_name
            )
            invoice.save()
            invoiceId = str(invoice.pk)
            return payment_repository_pb2.StoreInvoiceResponse(
                response_code=0,
                invoiceId=invoiceId,
                invoice=paymentHandler.getInvoice(invoiceId)
            )
        except NotUniqueError:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details('Invoice already exists')
            return payment_repository_pb2.StoreInvoiceResponse(response_code=1)

    def RetrieveInvoice(self, request, context):
        invoice = paymentHandler.getInvoice(request.invoiceId)
        if invoice:
            return payment_repository_pb2.StoreInvoiceResponse(
                response_code=0,
                invoiceId=invoice.invoiceId,
                invoice=invoice
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Invoice not found')
            return payment_repository_pb2.StoreInvoiceResponse(response_code=1)

    def GetUserInvoices(self, request, context):
        invoices = paymentHandler.getInvoices(request.userId)
        if invoices:
            return payment_repository_pb2.UserInvoicesResponse(invoices=invoices)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('No invoices found for user')
            return payment_repository_pb2.UserInvoicesResponse()
    
def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    payment_repository_pb2_grpc.add_UserRepositoryServicer_to_server(
        PaymentRepositoryService(), server
    )

    server.add_insecure_port("[::]:50064")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":

    __USER = os.getenv('MONGO_USER')
    __PASSWORD =  os.getenv('MONGO_PASSWORD')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@cluster0.q350jt0.mongodb.net/db?retryWrites=true&w=majority&appName=Cluster0"
    connect(host=url)

    serve()