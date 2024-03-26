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
from models.user import User
from mongoengine import *
import os

class UserRepositoryService(user_repository_pb2_grpc.UserRepositoryServicer):
    
    def InsertUser(self, request, context):

        username = request.username
        password = request.password
        address = request.address

        user = User(username=username, password=password, address=address)

        try:
            user.save()
            #Success
            return InsertUserResponse(response_code = 0)
        except NotUniqueError:
            #Repeated username
            return InsertUserResponse(response_code = 1)

    
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

    __USER = os.getenv('MONGO_USER')
    __PASSWORD =  os.getenv('MONGO_PASSWORD')
    url = f"mongodb+srv://{__USER}:{__PASSWORD}@cluster0.q350jt0.mongodb.net/db?retryWrites=true&w=majority&appName=Cluster0"
    connect(host=url)

    serve()