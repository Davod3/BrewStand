import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import payment_service_pb2
import payment_service_pb2_grpc

from payment_service_pb2 import (
    ProcessPaymentResponse,
    InvoiceResponse,
    UserInvoicesResponse
)

import handlers.paymentHandler as PaymentHandler
import handlers.invoiceHandler as InvoiceHandler

class PaymentService(payment_service_pb2_grpc.PaymentServicer):

    def ProcessPayment(self, request, context):

        response = PaymentHandler.process_payment(request.user_id, request.amount, request.currency, request.items_id, request.card_details )

        return ProcessPaymentResponse(response_code = response.response_code, invoice = response.invoice)

    def GetInvoice(self, request, context):
        
        response = InvoiceHandler.getInvoice()
        
        return InvoiceResponse(response_code = response.response_code, invoice=response.invoice)

    def GetUserInvoices(self, request, context):
        
        response = InvoiceHandler.getUserInvoices(userId = request.userId)
        
        return InvoiceResponse(response_code = response.response_code, invoice=response.invoice)
      
def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    payment_service_pb2_grpc.add_PaymentServicer_to_server(
        PaymentService(), server
    )

    server.add_insecure_port("[::]:50055")
    server.start()
    print("Payment Service running on port 50055")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
