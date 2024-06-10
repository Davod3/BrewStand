from concurrent import futures
import load_dataset
import grpc

import Handlers.inventoryHandler as inventoryHandler

import inventory_repository_pb2_grpc

from grpc_interceptor import ExceptionToStatusInterceptor

class InventoryRepository(inventory_repository_pb2_grpc.InventoryRepositoryServicer):

    def getBatchCost(self, request, context):

        return inventoryHandler.getBatchCost(request, context)

    def getBatchScore(self, request, context):
       
       return inventoryHandler.getBatchScore(request, context)

    def getBatchVolume(self, request, context):

        return inventoryHandler.getBatchVolume(request, context)


    def getBatchUsersReview(self, request, context):

        return inventoryHandler.getBatchUsersReview(request, context)

    def getBatch(self, request, context):

        return inventoryHandler.getBatch(request, context)

    def getBatches(self, request, context):

        return inventoryHandler.getBatches(request, context)

    def updateUserScore(self, request, context):
        
        return inventoryHandler.updateUserScore(request, context)


    def updateVolume(self, request, context):
     
        return inventoryHandler.updateVolume(request, context)

def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    inventory_repository_pb2_grpc.add_InventoryRepositoryServicer_to_server(
        InventoryRepository(), server
    )

    server.add_insecure_port("[::]:50062")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    load_dataset.load()
    serve()
