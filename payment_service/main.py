import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import payment_service_pb2
import payment_service_pb2_grpc

from payment_service_pb2 import (
    ProcessPaymentResponse,
    StoreInvoiceRequest,
    InvoiceResponse,
    UserInvoicesResponse
)

import paymentHandler

class PaymentService(payment_service_pb2_grpc.PaymentServicer):

    def ProcessPayment(self, request, context):
        # Process the payment
        payment_success, card_last_four = paymentHandler.process_payment(
            user_id=request.user_id,
            amount=request.amount,
            currency=request.currency,
            items_id=request.items_id,
            card_details=request.card_details 
        )

        if not payment_success:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Payment processing failed")
            return ProcessPaymentResponse(success=False)

        order_channel = grpc.insecure_channel('order_service_endpoint') 
        order_stub = order_service_pb2_grpc.OrderServiceStub(order_channel)
        order_response = order_stub.CreateOrder(...) 

        if not order_response.success:
            return payment_service_pb2.PaymentResponse(success=False)
        
        repository_channel = grpc.insecure_channel('repository_service_endpoint') 
        repository_stub = payment_repository_pb2_grpc.PaymentRepositoryServiceStub(repository_channel)
        invoice_data = payment_repository_pb2.InvoiceData(
            invoiceID=0,  # Assuming the ID is assigned by the repository
            price=request.amount,
            orderID=order_id,
            userID=request.user_id,
            fiscalAddress=request.fiscalAddress,
            details=""  # Add any required details
        )
        store_invoice_response = repository_stub.StoreInvoice(
            StoreInvoiceRequest(invoice=invoice_data)
        )

        if store_invoice_response.success:
            return payment_service_pb2.ProcessPaymentResponse(
                success=True,
                invoiceId=str(store_invoice_response.invoiceId),
                invoice=store_invoice_response.invoice
            )
        else:
            context.set_code(grpc.StatusCode.ABORTED)
            context.set_details("Failed to store invoice")
            return payment_service_pb2.ProcessPaymentResponse(success=False)

    def GetInvoice(self, request, context):
        # Integration with the repository service to retrieve an invoice
        repository_channel = grpc.insecure_channel('repository_service_endpoint')
        repository_stub = payment_repository_pb2_grpc.PaymentRepositoryServiceStub(repository_channel)
        try:
            retrieve_response = repository_stub.RetrieveInvoice(
                payment_repository_pb2.RetrieveInvoiceRequest(invoiceId=request.invoiceId)
            )
            return InvoiceResponse(
                success=True,
                invoice=retrieve_response
            )
        except grpc.RpcError as e:
            context.set_code(e.code())
            context.set_details(e.details())
            return payment_service_pb2.InvoiceResponse(success=False)
    
    def GetUserInvoices(self, request, context):
        # Integration with the repository service to retrieve user invoices
        repository_channel = grpc.insecure_channel('repository_service_endpoint')
        repository_stub = payment_repository_pb2_grpc.PaymentRepositoryServiceStub(repository_channel)
        try:
            user_invoices_response = repository_stub.GetUserInvoices(
                payment_repository_pb2.GetUserInvoicesRequest(userId=request.userId)
            )
            return payment_service_pb2.UserInvoicesResponse(
                invoices=user_invoices_response.invoices
            )
        except grpc.RpcError as e:
            context.set_code(e.code())
            context.set_details(e.details())
            return UserInvoicesResponse()

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
