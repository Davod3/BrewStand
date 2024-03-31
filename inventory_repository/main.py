from concurrent import futures
import load_dataset
import psycopg2
import grpc
import os

from inventory_repository_pb2 import (
    GetBatchResponse,
    GetBatchesResponse,
    GetBatchScoreResponse,
    GetBatchCostResponse,
    GetBatchUsersReviewResponse,
    BatchDetails,
    UpdateUserScoreResponse
)

import inventory_repository_pb2_grpc

from grpc_interceptor import ExceptionToStatusInterceptor

class InventoryRepository(inventory_repository_pb2_grpc.InventoryRepositoryServicer):

    def getBatchCost(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT cost FROM inventory WHERE batch_id = %s", [request.batch_id])
            result = cursor.fetchone()

            if result is not None:
                return GetBatchCostResponse(response_code=0, cost=float(result[0]))
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return GetBatchCostResponse(response_code=1, cost=0.0)
        except psycopg2.Error as e:
            print("Error retrieving batch cost:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetBatchCostResponse(response_code=-1, cost=0.0)
        finally:
            if conn:
                conn.close()

    def getBatchScore(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT user_score FROM inventory WHERE batch_id = %s", [request.batch_id])
            result = cursor.fetchone()

            if result is not None:
                return GetBatchScoreResponse(response_code=0, score=float(result[0]))
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return GetBatchScoreResponse(response_code=1 ,score=0.0)
        except psycopg2.Error as e:
            print("Error retrieving batch score:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetBatchScoreResponse(response_code=-1, score=0.0)
        finally:
            if conn:
                conn.close()

    def getBatchUsersReview(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT n_users_review FROM inventory WHERE batch_id = %s", [request.batch_id])
            result = cursor.fetchone()

            if result is not None:
                return GetBatchUsersReviewResponse(response_code=0, n_users_review=result[0])
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return GetBatchUsersReviewResponse(response_code=1,n_users_review=0)
        except psycopg2.Error as e:
            print("Error retrieving batch user review:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetBatchUsersReviewResponse(response_code=-1, review=0)
        finally:
            if conn:
                conn.close()

    def getBatch(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM inventory WHERE batch_id = %s", [request.batch_id])
            result = cursor.fetchone()

            if result is not None:

                batch_info = BatchDetails(
                    batch_id=int(result[0]),
                    brew_date=str(result[1]),
                    beer_style=result[2],
                    location=result[3],
                    ph_level=float(result[4]),
                    alcohol_content=float(result[5]),
                    volume_produced=float(result[6]),
                    quality_score=float(result[7]),
                    cost=float(result[8]),
                    user_score=float(result[9]),
                    n_users_review=int(result[10])
                ) 

                response = GetBatchResponse(
                    response_code = 0,
                    batch = batch_info
                )

                return response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return GetBatchResponse(response_code=1)
        except psycopg2.Error as e:
            print("Error retrieving batch info:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetBatchResponse(response_code=-1)
        finally:
            if conn:
                conn.close()

    def getBatches(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM inventory")
            result = cursor.fetchall()

            if result is not None:

                items = list()

                for item in result:

                    batch_info = BatchDetails(
                        batch_id=int(item[0]),
                        brew_date=str(item[1]),
                        beer_style=item[2],
                        location=item[3],
                        ph_level=float(item[4]),
                        alcohol_content=float(item[5]),
                        volume_produced=float(item[6]),
                        quality_score=float(item[7]),
                        cost=float(item[8]),
                        user_score=float(item[9]),
                        n_users_review=int(item[10])
                    )

                    items.append(batch_info)

                response = GetBatchesResponse(
                    response_code = 0,
                    batches = items
                )

                return response
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return GetBatchesResponse(response_code=1, batches=[])
        except psycopg2.Error as e:
            print("Error retrieving batch info:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return GetBatchesResponse(response_code=-1, batches=[])
        finally:
            if conn:
                conn.close()

    def updateUserScore(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("UPDATE inventory SET user_score = %s WHERE batch_id = %s", [request.new_score, request.batch_id])
            conn.commit()

            cursor.execute("UPDATE INVENTORY SET n_users_review = n_users_review + 1 WHERE batch_id = %s", [request.batch_id])
            conn.commit()
            
            if cursor.rowcount > 0:
                return UpdateUserScoreResponse(response_code = 0)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return UpdateUserScoreResponse(response_code = 1)
        except psycopg2.Error as e:
            print("Error updating batch score:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return UpdateUserScoreResponse(response_code = -1)
        finally:
            if conn:
                conn.close()

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
