import os
import grpc

import handlers.userHandler as UserHandler

from payment_service_pb2 import (
    PaymentRequest,
    CardDetails
)

from payment_service_pb2_grpc import PaymentServiceStub

#payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
#payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50052")
#user_repository_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

#client = PaymentServiceStub(user_repository_channel)

def initiatePayment(user_id, card_number, card_expiry, card_cvc):

    response_code = 0
    invoice_id = 0
    price = 0
    order_id = 0
    customer_id = ''
    fiscal_address = ''
    details = ''

    #Get cart contents
    (code, cart_contents, cost) = UserHandler.getCartContent(user_id)

    if(code == 0):

        user = UserHandler.getUserByID(user_id)

        if(len(cart_contents) > 0):

            items = list()

            for cart_item in cart_contents:
                items.append(cart_item.batch_id)

            '''
            UNCOMMENT WHEN PAYMENT SERVICE IS READY

            request = PaymentRequest(user_id = user_id,
                                     amount = cost,
                                     currency = 'EUR',
                                     items_id = items,
                                     card_details = CardDetails(card_number=card_number,
                                                                card_expiry=card_expiry,
                                                                card_cvc=card_cvc))
            
            response = client.ProcessPayment(request)

            if(response.success):
                #Prepare response

                invoice_id = 0
                price = response.invoice.invoice_details.amount
                order_id = response.invoice.order_id
                customer_id = response.invoice.user_id
                fiscal_address = user.address
                details = f"{response.invoice.invoice_details.currency}:{response.invoice.invoice_details.card_last_four}"

            else:
                # Invalid Order
                response_code = 3

                '''

        else:
            # Cart is empty
            response_code = 2

    else:
        #User not found
        response_code = 1

    return (response_code,
            invoice_id,
            price,
            order_id,
            customer_id,
            fiscal_address,
            details)