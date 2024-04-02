from concurrent import futures
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound


import payment_service_pb2
import payment_service_pb2_grpc

from payment_service_pb2 import (
    ProcessPaymentResponse,
    InvoiceResponse,
    InvoicesResponse
)

import handlers.paymentHandler as PaymentHandler
import handlers.invoiceHandler as InvoiceHandler

class PaymentService(payment_service_pb2_grpc.PaymentService):

    def ProcessPayment(self, request):

        response = PaymentHandler.process_payment(request.user_id, request.amount, request.currency, request.items_id, request.card_details )

        return ProcessPaymentResponse(response_code = response.response_code, invoice = response.invoice)

    def GetInvoice(self, request):
        invoice = InvoiceHandler.getInvoice(request.invoiceId)
        
        return InvoiceResponse(
            invoiceId=invoice.invoiceId,
            price=invoice.price,
            orderId=invoice.orderId,
            customerId=invoice.customerId,
            fiscalAddress=invoice.fiscalAddress,
            details=invoice.details
        )
    
    def GetAllUserInvoices(self, request, context):
        invoices = InvoiceHandler.getUserInvoices(request.userId)  
        return InvoicesResponse(
            invoices=[
                InvoiceResponse(
                    invoiceId=inv.invoiceId,
                    price=inv.price,
                    orderId=inv.orderId,
                    customerId=inv.customerId,
                    fiscalAddress=inv.fiscalAddress,
                    details=inv.details
                ) for inv in invoices
            ]
        )


def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    payment_service_pb2_grpc.add_PaymentServiceServicer_to_server(
        PaymentService(), server
    )

    server.add_insecure_port("[::]:50055")
    server.start()
    print("Payment Service running on port 50055")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
