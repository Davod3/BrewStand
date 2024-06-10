from concurrent import futures
import os
import grpc
import handlers.inventoryServiceHandler as inventoryHandler

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

import inventory_service_pb2_grpc

class InventoryService(inventory_service_pb2_grpc.InventoryServiceServicer):

    def validateItemService(self, request, context):
        
        return inventoryHandler.validateItemService(request,context)

    def getBatchCostService(self, request, context):
        
        return inventoryHandler.getBatchCostService(request, context)
    
    def getBatchScoreService(self, request, context):
        
        return inventoryHandler.getBatchScoreService(request, context)

    def getBatchUsersReviewService(self, request, context):
        
        return inventoryHandler.getBatchUsersReviewService(request, context)

    def getBatchService(self, request, context):
        
        return inventoryHandler.getBatchService(request, context)
        
    def getBatchesService(self, request, context):

        return inventoryHandler.getBatchesService(request, context)

    def updateScoreService(self, request, context):
        
        return inventoryHandler.updateScoreService(request, context)

    def validateOrderService(self, request, context):
        
        return inventoryHandler.validateOrderService(request, context)
        
    def updateVolumeService(self, request, context):
        
        return inventoryHandler.updateVolumeService(request, context)

def serve():
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    inventory_service_pb2_grpc.add_InventoryServiceServicer_to_server(
        InventoryService(), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
