import connexion
import six

import os
import grpc

from user_service_pb2 import (
    TradeTokenRequest
)

from user_service_pb2_grpc import UserStub

user_service_host = os.getenv("USER_SERVICE_HOST", "localhost")
user_service_port = os.getenv("USER_SERVICE_PORT", "50051")
user_service_channel = grpc.insecure_channel(f"{user_service_host}:{user_service_port}")

client = UserStub(user_service_channel)

def tradeToken(token):

    request = TradeTokenRequest(token = token)
    response = client.TradeToken(request)


    if(response.response_code == 0):
        return {'user_id' : response.user_id}
    else:
        return None