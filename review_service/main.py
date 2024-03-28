from concurrent import futures

import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from review_service_pb2 import(
    ItemReviewResponse,
)

import review_service_pb2_grpc
import review_service.handlers.reviewHandler as reviewHandler

class ReviewService (review_service_pb2_grpc.ReviewServicer):

    def ReviewItem(self, request, context):

        result = reviewHandler.validScore(request.item_id, request.score)
        return ItemReviewResponse(response_code=result)

def serve():

    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10), interceptors=interceptors
    )

    review_service_pb2_grpc.add_ReviewServicer_to_server(
        ReviewService(), server
    )

    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()