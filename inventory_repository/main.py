import load_dataset

import inventory_repository_pb2
import psycopg2
import grpc
import os
from concurrent import futures

class InventoryRepositoryService(inventory_repository_pb2.InventoryRepositoryServicer): #grpc

    def __init__(self):
        pass

    def validateItem(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result[0] > 0:
                return inventory_repository_pb2.ValidationResponse(valid=True)
            else:
                return inventory_repository_pb2.ValidationResponse(valid=False)
        except psycopg2.Error as e:
            print("Error validating item:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.ValidationResponse(valid=False)
        finally:
            if conn:
                conn.close()

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

            cursor.execute("SELECT cost FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result is not None:
                return inventory_repository_pb2.CostResponse(cost=float(result[0]))
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.CostResponse(cost=0.0)
        except psycopg2.Error as e:
            print("Error retrieving batch cost:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.CostResponse(cost=0.0)
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

            cursor.execute("SELECT user_score FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result is not None:
                return inventory_repository_pb2.ScoreResponse(score=float(result[0]))
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.ScoreResponse(score=0.0)
        except psycopg2.Error as e:
            print("Error retrieving batch score:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.ScoreResponse(score=0.0)
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

            cursor.execute("SELECT user_review FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result is not None:
                return inventory_repository_pb2.ReviewResponse(review=result[0])
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.ReviewResponse(review="No reviews available")
        except psycopg2.Error as e:
            print("Error retrieving batch user review:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.ReviewResponse(review="No reviews available")
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

            cursor.execute("SELECT * FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result is not None:
                batch_info = inventory_repository_pb2.BatchInfo(
                    batch_id=result[0],
                    brew_date=str(result[1]),
                    beer_style=result[2],
                    location=result[3],
                    ph_level=float(result[4]),
                    alcohol_content=float(result[5]),
                    volume_produced=float(result[6]),
                    quality_score=float(result[7]),
                    cost=float(result[8]),
                    user_score=float(result[9]),
                    n_users_review=float(result[10])
                )
                return batch_info
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.BatchInfo()
        except psycopg2.Error as e:
            print("Error retrieving batch info:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.BatchInfo()
        finally:
            if conn:
                conn.close()

    def getCompareBatches(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM inventory WHERE batch_id IN (%s, %s)", (request.batch_id1, request.batch_id2))
            result = cursor.fetchall()

            if result is not None and len(result) == 2:
                batch1_info = inventory_repository_pb2.BatchInfo(
                    batch_id=result[0][0],
                    brew_date=str(result[0][1]),
                    beer_style=result[0][2],
                    location=result[0][3],
                    ph_level=float(result[0][4]),
                    alcohol_content=float(result[0][5]),
                    volume_produced=float(result[0][6]),
                    quality_score=float(result[0][7]),
                    cost=float(result[0][8]),
                    user_score=float(result[0][9]),
                    n_users_review=float(result[0][10])
                )
                batch2_info = inventory_repository_pb2.BatchInfo(
                    batch_id=result[1][0],
                    brew_date=str(result[1][1]),
                    beer_style=result[1][2],
                    location=result[1][3],
                    ph_level=float(result[1][4]),
                    alcohol_content=float(result[1][5]),
                    volume_produced=float(result[1][6]),
                    quality_score=float(result[1][7]),
                    cost=float(result[1][8]),
                    user_score=float(result[1][9]),
                    n_users_review=float(result[1][10])
                )
                comparison_info = inventory_repository_pb2.ComparisonInfo(
                    batch1=batch1_info,
                    batch2=batch2_info
                )
                return comparison_info
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("One or both batches not found")
                return inventory_repository_pb2.ComparisonInfo()
        except psycopg2.Error as e:
            print("Error retrieving batch comparison info:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.ComparisonInfo()
        finally:
            if conn:
                conn.close()

    def updateScore(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("UPDATE inventory SET user_score = %s WHERE batch_id = %s", (request.new_score, request.batch_id))
            conn.commit()

            if cursor.rowcount > 0:
                return inventory_repository_pb2.UpdateScoreResponse(success=True)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.UpdateScoreResponse(success=False)
        except psycopg2.Error as e:
            print("Error updating batch score:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.UpdateScoreResponse(success=False)
        finally:
            if conn:
                conn.close()

    def validateOrder(self, request, context):
        try:
            conn = psycopg2.connect(
                dbname=os.getenv('INVENTORY_DB_NAME'),
                user=os.getenv('INVENTORY_DB_USER'),
                password=os.getenv('INVENTORY_DB_PASSWORD'),
                host=os.getenv('INVENTORY_DB_HOST'),
                port=os.getenv('INVENTORY_DB_PORT')
            )
            cursor = conn.cursor()

            cursor.execute("SELECT volume_produced FROM inventory WHERE batch_id = %s", (request.batch_id,))
            result = cursor.fetchone()

            if result is not None:
                volume_produced = result[0]
                if volume_produced >= request.quantity:
                    return inventory_repository_pb2.OrderValidationResponse(valid=True)
                else:
                    return inventory_repository_pb2.OrderValidationResponse(valid=False)
            else:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Batch not found")
                return inventory_repository_pb2.OrderValidationResponse(valid=False)
        except psycopg2.Error as e:
            print("Error validating order:", e)
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error")
            return inventory_repository_pb2.OrderValidationResponse(valid=False)
        finally:
            if conn:
                conn.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inventory_repository_pb2.add_InventoryRepositoryServicer_to_server( #grpc
        InventoryRepositoryService(), server
    )
    server.add_insecure_port("[::]:50061")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    load_dataset.load()
    serve()
