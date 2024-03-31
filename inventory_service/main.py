import grpc
from concurrent import futures
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound
from inventory_repository.main import InventoryRepositoryService
from mongoengine import *

from inventory_service_pb2 import (
    validateItemResponse,
    getBatchCostResponse,
    getBatchScoreResponse,
    getBatchUsersReviewResponse,
    getBatchResponse,
    getCompareBatchesResponse,
    updateScoreResponse,
    validateOrderResponse
)
import inventory_repository_pb2
import inventory_repository_pb2_grpc

class InventoryService(inventory_repository_pb2_grpc.InventoryRepositoryServicer):

    def __init__(self):
        pass

    def validateItem(self, request, context):
        response = inventory_repository_pb2.ValidationResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.validateItem(request)
        except grpc.RpcError as e:
            print("Error calling validateItem:", e.details())
            response.valid = False
        return response

    def getBatchCost(self, request, context):
        response = inventory_repository_pb2.CostResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.getBatchCost(request)
        except grpc.RpcError as e:
            print("Error calling getBatchCost:", e.details())
            response.cost = 0.0
        return response

    def getBatchScore(self, request, context):
        response = inventory_repository_pb2.ScoreResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.getBatchScore(request)
        except grpc.RpcError as e:
            print("Error calling getBatchScore:", e.details())
            response.score = 0.0
        return response

    def getBatchUsersReview(self, request, context):
        response = inventory_repository_pb2.ReviewResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.getBatchUsersReview(request)
        except grpc.RpcError as e:
            print("Error calling getBatchUsersReview:", e.details())
            response.review = "No reviews available"
        return response

    def getBatch(self, request, context):
        response = inventory_repository_pb2.BatchInfo()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.getBatch(request)
        except grpc.RpcError as e:
            print("Error calling getBatch:", e.details())
            response = inventory_repository_pb2.BatchInfo()
        return response

    def getCompareBatches(self, request, context):
        response = inventory_repository_pb2.ComparisonInfo()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.getCompareBatches(request)
        except grpc.RpcError as e:
            print("Error calling getCompareBatches:", e.details())
            response = inventory_repository_pb2.ComparisonInfo()
        return response

    def updateScore(self, request, context):
        response = inventory_repository_pb2.UpdateScoreResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.updateScore(request)
        except grpc.RpcError as e:
            print("Error calling updateScore:", e.details())
            response.success = False
        return response

    def validateOrder(self, request, context):
        response = inventory_repository_pb2.OrderValidationResponse()
        try:
            channel = grpc.insecure_channel('localhost:50061')
            stub = inventory_repository_pb2_grpc.InventoryRepositoryStub(channel)
            response = stub.validateOrder(request)
        except grpc.RpcError as e:
            print("Error calling validateOrder:", e.details())
            response.valid = False
        return response

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    inventory_repository_pb2_grpc.add_InventoryRepositoryServicer_to_server(
        InventoryRepositoryService(), server
    )

    server.add_insecure_port("[::]:50061")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
