import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import payment_service_pb2
import payment_service_pb2_grpc

from payment_service_pb2 import (
    PaymentRequest,
    PaymentResponse,
    InvoiceRequest,
    InvoiceResponse,
    UserInvoicesRequest,
    UserInvoicesResponse,
)

import paymentHandler

class PaymentService(payment_service_pb2_grpc.PaymentServicer):

    def ProcessPayment(self, request, context):
        payment_success, card_last_four = paymentHandler.process_payment(
            user_id=request.user_id,
            amount=request.amount,
            currency=request.currency,
            items_id=request.items_id,
            card_details=request.card_details 
        )

        if not payment_success:
            return payment_service_pb2.PaymentResponse(success=False)

        order_channel = grpc.insecure_channel('order_service_endpoint') 
        order_stub = order_service_pb2_grpc.OrderServiceStub(order_channel)
        order_response = order_stub.CreateOrder(...) 

         if not order_response.success:
            return payment_service_pb2.PaymentResponse(success=False)

        repository_channel = grpc.insecure_channel('')
        repository_stub = payment_repository_pb2_grpc.PaymentRepositoryServiceStub(repository_channel)
        invoice_data = payment_repository_pb2.InvoiceData(
            payment_details=payment_repository_pb2.PaymentData(
                amount=request.amount,
                currency=request.currency,
                item_ids=request.items_id,
                card_last_four=card_last_four  # Here you use the obtained last four digits
            ),
            user_id=request.user_id,
            order_id=order_response.order_id
        )
        store_invoice_response = repository_stub.StoreInvoice(invoice_data)

        if store_invoice_response:
            return payment_service_pb2.PaymentResponse(
                success=True
                invoice_data=invoice_data
            )

        else:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Payment processing failed")
            return payment_service_pb2.PaymentResponse(success=False)


    def GetInvoice(self, request, context):
        try:
            invoice_data = retrieve_invoice(request.order_id)
            return payment_service_pb2.InvoiceResponse(
                success=True,
                invoice=invoice_data
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return payment_service_pb2.InvoiceResponse(success=False)
    
    def GetUserInvoices(self, request, context):
        try:
            return payment_service_pb2.UserInvoicesResponse(invoices=invoices)
        except NotFound:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User invoices not found')
            return payment_service_pb2.UserInvoicesResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return payment_service_pb2.UserInvoicesResponse()

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    payment_service_pb2_grpc.add_PaymentServicer_to_server(
        PaymentService(), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    print("Payment Service running on port 50052")
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
