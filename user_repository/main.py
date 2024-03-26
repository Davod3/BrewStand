from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from user_pb2 import (
    CreateUserResponse
)

import user_pb2_grpc

class UserService(user_pb2_grpc.UserServicer):
    
    def CreateUser(self, request, context):
        # Do some magic
        return CreateUserResponse(response_code = 0)
    
def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    user_pb2_grpc.add_UserServicer_to_server(
        UserService(), server
    )

    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()