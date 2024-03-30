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

def initiatePayment(user_id):

    return None