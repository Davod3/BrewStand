from concurrent import futures
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
    UpdateUserScoreResponse,
    GetVolumeResponse,
    UpdateVolumeResponse
)

def getBatchCost(request, context):
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
        return GetBatchCostResponse(response_code=1, cost=0.0)
    finally:
        if conn:
            conn.close()
    
def getBatchScore(request, context):
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
        return GetBatchScoreResponse(response_code=1, score=0.0)
    finally:
        if conn:
            conn.close()

def getBatchVolume(request, context):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('INVENTORY_DB_NAME'),
            user=os.getenv('INVENTORY_DB_USER'),
            password=os.getenv('INVENTORY_DB_PASSWORD'),
            host=os.getenv('INVENTORY_DB_HOST'),
            port=os.getenv('INVENTORY_DB_PORT')
        )
        cursor = conn.cursor()

        cursor.execute("SELECT volume_produced FROM inventory WHERE batch_id = %s", [request.batch_id])
        result = cursor.fetchone()

        if result is not None:
            
            volume_produced = float(result[0])
            return GetVolumeResponse(response_code=0, volume=volume_produced)
        
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Batch not found")
            return GetVolumeResponse(response_code=1, volume=0.0)
    except psycopg2.Error as e:
        print("Error retrieving batch volume:", e)
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Internal server error")
        return GetVolumeResponse(response_code=1, volume=0.0)
    finally:
        if conn:
            conn.close()

def getBatchUsersReview(request, context):
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
        return GetBatchUsersReviewResponse(response_code=1, review=0)
    finally:
        if conn:
            conn.close()
    
def getBatch(request, context):
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
        return GetBatchResponse(response_code=1)
    finally:
        if conn:
            conn.close()

def getBatches(request, context):
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
        return GetBatchesResponse(response_code=1, batches=[])
    finally:
        if conn:
            conn.close()

def updateUserScore(request, context):
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
        return UpdateUserScoreResponse(response_code = 1)
    finally:
        if conn:
            conn.close()

def updateVolume(request, context):
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('INVENTORY_DB_NAME'),
            user=os.getenv('INVENTORY_DB_USER'),
            password=os.getenv('INVENTORY_DB_PASSWORD'),
            host=os.getenv('INVENTORY_DB_HOST'),
            port=os.getenv('INVENTORY_DB_PORT')
        )
        cursor = conn.cursor()

        cursor.execute("UPDATE inventory SET volume_produced = %s WHERE batch_id = %s", [request.volume_order, request.batch_id])
        conn.commit()
        
        if cursor.rowcount > 0:
            return UpdateVolumeResponse(response_code = 0)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Batch not found")
            return UpdateVolumeResponse(response_code = 1)
    except psycopg2.Error as e:
        print("Error updating batch score:", e)
        context.set_code(grpc.StatusCode.INTERNAL)
        context.set_details("Internal server error")
        return UpdateVolumeResponse(response_code = 1)
    finally:
        if conn:
            conn.close()