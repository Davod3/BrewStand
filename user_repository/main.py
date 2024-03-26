from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from user_repository_pb2 import (
    InsertUserResponse,
    UserCartAddResponse,
    UserCartDeleteResponse,
    UserCartGetResponse
)

import user_repository_pb2_grpc

class UserRepositoryService(user_repository_pb2_grpc.UserRepositoryServicer):
    
    def InsertUser(self, request, context):
        # Do some magic
        return InsertUserResponse(response_code = 0)
    
    def UserCartAdd(self,request, context):
        # Do some magic
        return UserCartAddResponse(response_code = 0)
    
    def UserCartDelete(self, request, context):
        return UserCartDeleteResponse(response_code = 0)
    
    def UserCartGet(self, request, context):
        return UserCartGetResponse(response_code = 0, total_cost = 0, content = None)
    
def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    user_repository_pb2_grpc.add_UserRepositoryServicer_to_server(
        UserRepositoryService(), server
    )

    server.add_insecure_port("[::]:50061")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()