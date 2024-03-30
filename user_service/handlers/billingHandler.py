import os
import grpc


from payment_service_pb2 import (
    PaymentRequest,
    CardDetails
)

from payment_service_pb2_grpc import PaymentServiceStub

#payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
#payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50052")
#user_repository_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

#client = PaymentServiceStub(user_repository_channel)

def initiatePayment(user_id, card_number, card_expiry, card_cvc):

    #Get user_id and card_details
    #Get cart contents

    response_code = 0
    invoice_id = 123
    price = 0
    order_id = 0
    customer_id = ''
    fiscal_address = ''
    details = ''

    return (response_code,
            invoice_id,
            price,
            order_id,
            customer_id,
            fiscal_address,
            details)