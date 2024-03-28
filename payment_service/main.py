import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import payment_service_pb2
import payment_service_pb2_grpc
import paymentHandler
import invoiceHandler

class PaymentService(payment_service_pb2_grpc.PaymentServicer):

    def ProcessPayment(self, request, context):
        payment_result = paymentHandler.process_payment(
            user_id=request.user_id,
            amount=request.amount,
            currency=request.currency,
            items_id=request.items_id,
            card_details=request.card_details
        )

        if payment_result[0]:
            return payment_service_pb2.PaymentResponse(
                success=True,
                payment_details=payment_result[1]
            )
        else:
            return payment_service_pb2.PaymentResponse(success=False)

    def GetInvoice(self, request, context):
        try:
            invoice_data = invoiceHandler.retrieve_invoice(request.invoice_id)
            return payment_service_pb2.InvoiceResponse(
                success=True,
                invoice=invoice_data
            )
        except Exception as e:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(str(e))
            return payment_service_pb2.InvoiceResponse(success=False)

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
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
