import connexion
import six

from models.item import Item  # noqa: E501
from utils import util

import os
import grpc

from prometheus_client import Counter, Summary

total_received_requests_metric = Counter('inventory_total_received_requests', 'Total number of requests received by the Inventory API')

duration_get_batch = Summary('duration_get_batch_seconds', 'Average time in seconds it takes for a user to receive a batch')
duration_get_batches = Summary('duration_get_batches_seconds', 'Average time in seconds it takes for a user to receive the full catalog')

failures_get_batch = Counter('failures_get_batch', 'Number of failures when a user gets a batch')
failures_get_batches = Counter('failures_get_batches', 'Number of failures when a user gets the full catalog')


from inventory_service_pb2 import (
    GetBatchServiceRequest,
    EmptyMessage
)

from inventory_service_pb2_grpc import InventoryServiceStub

inventory_service_host = os.getenv("INVENTORY_SERVICE_HOST", "localhost")
inventory_service_port = os.getenv("INVENTORY_SERVICE_PORT", "50052")
inventory_service_channel = grpc.insecure_channel(f"{inventory_service_host}:{inventory_service_port}")

client = InventoryServiceStub(inventory_service_channel) 

def __parseBatch(batch):

    parsed_batch = Item.from_dict({
                    "batchID" : batch.batch_id,
                    "brewLocation" : batch.location,
                    "beerStyle" : batch.beer_style,
                    "userScore" : batch.user_score,
                    "expertScore" : batch.quality_score,
                    "phLevel" : batch.ph_level,
                    "alchoolContent" : batch.alcohol_content,
                    "availableVolume" : batch.volume_produced,
                    "brewDate" : batch.brew_date,
                    "cost" : batch.cost
                })
    
    return parsed_batch

@duration_get_batch.time()
@failures_get_batch.count_exceptions()
def getBatch(itemId):

    total_received_requests_metric.inc()

    request = GetBatchServiceRequest(batch_id = itemId)
    response = client.getBatchService(request)

    if(response.response_code == 0):

        return __parseBatch(response.batch), 200
    else:

        #Not found
        return 'Item not found!', 404

@duration_get_batches.time()
@failures_get_batches.count_exceptions()
def getBatches(item1=None, item2=None):

    total_received_requests_metric.inc()

    if(item1 is not None and item2 is not None):

        request_batch1 = GetBatchServiceRequest(batch_id = item1)
        response_batch1 = client.getBatchService(request_batch1)

        request_batch2 = GetBatchServiceRequest(batch_id = item2)
        response_batch2 = client.getBatchService(request_batch2)

        if(response_batch1.response_code == 0 and response_batch2.response_code == 0):
            
            batch1 = __parseBatch(response_batch1.batch)
            batch2 = __parseBatch(response_batch2.batch)

            return [batch1, batch2]

        else:

            #Not found
            return [], 404
    else:

        batches = list()

        request = EmptyMessage()
        response = client.getBatchesService(request)

        if(response.response_code == 0):

            for batch in response.batches:

                batches.append(__parseBatch(batch))
            
            return batches, 200

        else:
            return 'Error fetching inventory!', 500
