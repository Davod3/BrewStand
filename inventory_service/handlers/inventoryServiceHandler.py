from concurrent import futures
import os
import grpc

from inventory_service_pb2 import (
    
    GetBatchServiceResponse,
    GetBatchScoreServiceResponse,
    GetBatchCostServiceResponse,
    GetBatchUsersReviewServiceResponse,
    ValidateItemServiceResponse,
    UpdateScoreServiceResponse,
    ValidateOrderServiceResponse,
    BatchDetailsService,
    GetBatchesServiceResponse,
    UpdateVolumeServiceResponse

)

#------Repository Imports-------

from inventory_repository_pb2_grpc import InventoryRepositoryStub

from inventory_repository_pb2 import (

    GetBatchRequest,
    GetBatchScoreRequest,
    GetBatchCostRequest,
    GetBatchUsersReviewRequest,
    UpdateUserScoreRequest,
    UpdateVolumeRequest,
    GetVolumeRequest,
    Empty

)

#-------------------------------

inventory_repository_host = os.getenv("INVENTORY_REPOSITORY_HOST", "localhost")
inventory_repository_port = os.getenv("INVENTORY_REPOSITORY_PORT", "50062")
inventory_repository_channel = grpc.insecure_channel(f"{inventory_repository_host}:{inventory_repository_port}")

client = InventoryRepositoryStub(inventory_repository_channel)

def validateItemService(request, context):
    try:
            repo_request = GetBatchRequest(batch_id = request.batch_id)
            repo_response = client.getBatch(repo_request)

            if(repo_response.response_code == 0):

                #Success
                return ValidateItemServiceResponse(response_code = 0)
        
            else:

                #Fail
                return ValidateItemServiceResponse(response_code = 1)

    except grpc.RpcError as e:
        
        print("Error calling validateItem:", e.details())
        return ValidateItemServiceResponse(response_code = 1)

def getBatchCostService(request, context):
    try:
            
            repo_request = GetBatchCostRequest(batch_id = request.batch_id)
            repo_response = client.getBatchCost(repo_request)

            if(repo_response.response_code == 0):

                #Success
                return GetBatchCostServiceResponse(response_code = 0,
                                                    cost = repo_response.cost)
        
            else:

                #Fail
                return GetBatchCostServiceResponse(response_code = 1)

        
    except grpc.RpcError as e:
        print("Error calling getBatchCost:", e.details())
        return GetBatchCostServiceResponse(response_code = 1)

def getBatchScoreService(request, context):
    try:
            
        repo_request = GetBatchScoreRequest(batch_id = request.batch_id)
        repo_response = client.getBatchScore(repo_request)

        if(repo_response.response_code == 0):

            #Success
            return GetBatchScoreServiceResponse(response_code = 0,
                                                score = repo_response.score)
    
        else:

            #Fail
            return GetBatchScoreServiceResponse(response_code = 1)
        
    except grpc.RpcError as e:
        print("Error calling getBatchScore:", e.details())
        return GetBatchScoreServiceResponse(response_code = 1)

def getBatchUsersReviewService(request, context):
     
    try:
            
            repo_request = GetBatchUsersReviewRequest(batch_id = request.batch_id)
            repo_response = client.getBatchUsersReview(repo_request)

            if(repo_response.response_code == 0):

                #Success
                return GetBatchUsersReviewServiceResponse(response_code = 0,
                                                    n_users_review = repo_response.n_users_review)
        
            else:

                #Fail
                return GetBatchUsersReviewServiceResponse(response_code = 1)

        
    except grpc.RpcError as e:
        print("Error calling getBatchUsersReview:", e.details())
        return GetBatchUsersReviewServiceResponse(response_code = 1)
    
def getBatchService(request, context):
     
    try:
            
            repo_request = GetBatchRequest(batch_id = request.batch_id)
            repo_response = client.getBatch(repo_request)

            if(repo_response.response_code == 0):
                
                batch_details = BatchDetailsService(batch_id = repo_response.batch.batch_id,
                                                    brew_date = repo_response.batch.brew_date,
                                                    beer_style = repo_response.batch.beer_style,
                                                    location = repo_response.batch.location,
                                                    ph_level = repo_response.batch.ph_level,
                                                    alcohol_content = repo_response.batch.alcohol_content,
                                                    volume_produced = repo_response.batch.volume_produced,
                                                    quality_score = repo_response.batch.quality_score,
                                                    cost = repo_response.batch.cost,
                                                    user_score = repo_response.batch.user_score,
                                                    n_users_review = repo_response.batch.n_users_review)

                #Success
                return GetBatchServiceResponse(response_code = 0,
                                                batch = batch_details)
            else:

                #Fail
                return GetBatchServiceResponse(response_code = 1)
        
    except grpc.RpcError as e:
        print("Error calling getBatchService:", e.details())
        return GetBatchServiceResponse(response_code = 1)
    
def getBatchesService(request, context):
     
    try:
            
        repo_request = Empty()
        repo_response = client.getBatches(repo_request)

        if(repo_response.response_code == 0):

            batches_service = list()

            for batch in repo_response.batches:

                batch_details = BatchDetailsService(batch_id = batch.batch_id,
                                                    brew_date = batch.brew_date,
                                                    beer_style = batch.beer_style,
                                                    location = batch.location,
                                                    ph_level = batch.ph_level,
                                                    alcohol_content = batch.alcohol_content,
                                                    volume_produced = batch.volume_produced,
                                                    quality_score = batch.quality_score,
                                                    cost = batch.cost,
                                                    user_score = batch.user_score,
                                                    n_users_review = batch.n_users_review)
                
                batches_service.append(batch_details)

            #Success
            return GetBatchesServiceResponse(response_code = 0,
                                            batches = batches_service)
    
        else:

            #Fail
            return GetBatchesServiceResponse(response_code = 1, batches=[])

        
    except grpc.RpcError as e:
        print("Error calling getBatchesService:", e.details())
        return GetBatchesServiceResponse(response_code = 1,batches=[])

def updateScoreService(request, context):
        try:
            
            repo_request = UpdateUserScoreRequest(batch_id = request.batch_id, new_score = request.new_score)
            repo_response = client.updateUserScore(repo_request)

            if(repo_response.response_code == 0):

                #Success
                return UpdateScoreServiceResponse(response_code = 0)
        
            else:

                #Fail
                return UpdateScoreServiceResponse(response_code = 1)

        
        except grpc.RpcError as e:
            print("Error calling updateScoreService:", e.details())
            return UpdateScoreServiceResponse(response_code = 1)
        
def validateOrderService(request, context):
    try:
        repo_request = GetVolumeRequest(batch_id = request.batch_id)
        repo_response = client.getBatchVolume(repo_request)

        if(repo_response.response_code == 0):

            #Success

            if(request.volume_order > repo_response.volume):

                #Volume exceeds available, invalid order
                return ValidateOrderServiceResponse(response_code = 1)
            
            else:

                #Volume is available, confirm it
                return ValidateOrderServiceResponse(response_code = 0)
    
        else:

            #Fail
            return ValidateOrderServiceResponse(response_code = 1)

    except grpc.RpcError as e:
        
        print("Error calling validateOrder:", e.details())
        return ValidateOrderServiceResponse(response_code = 1)

def updateVolumeService(request, context):
    try:
        repo_request = GetVolumeRequest(batch_id = request.batch_id)
        repo_response = client.getBatchVolume(repo_request)

        if(repo_response.response_code == 0):

            #Success - Subtract order volume from current inventory
            repo_update_request = UpdateVolumeRequest(batch_id = request.batch_id,
                                                        volume_order = repo_response.volume - request.volume)

            repo_update_response = client.updateVolume(repo_update_request)

            if(repo_update_response.response_code == 0):

                return UpdateVolumeServiceResponse(response_code = 0)
            
            else:

                return UpdateVolumeServiceResponse(response_code = 1)
    
        else:

            #Fail
            return UpdateVolumeServiceResponse(response_code = 1)

    except grpc.RpcError as e:
        
        print("Error calling validateOrder:", e.details())
        return UpdateVolumeServiceResponse(response_code = 1)