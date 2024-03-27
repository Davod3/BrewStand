import os
import grpc

from review_service_pb2 import(
    ItemReviewRequest,
)

def validID(id):
    return True

def validScore(id,score):
    if (validID(id) and 0<=score<6):
        request = ItemReviewRequest(id= id,score=score)
        response = true ## não sei o que meter aqui

        return response.response_code