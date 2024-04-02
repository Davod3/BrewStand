import os
import grpc

import handlers.userHandler as UserHandler

from payment_service_pb2 import (
    ProcessPaymentRequest,
    CardDetails, 
    Items
)

from payment_service_pb2_grpc import PaymentServiceStub

payment_service_host = os.getenv("PAYMENT_SERVICE_HOST", "localhost")
payment_service_port = os.getenv("PAYMENT_SERVICE_PORT", "50055")
payment_service_channel = grpc.insecure_channel(f"{payment_service_host}:{payment_service_port}")

client = PaymentServiceStub(payment_service_channel)

def initiatePayment(user_id, card_number, card_expiry, card_cvc):

    #Default values
    response_code = 0
    invoice_id = ''
    price = 0
    order_id = ''
    customer_id = ''
    fiscal_address = ''
    details = ''

    #Get cart contents
    (code, cart_contents, cost) = UserHandler.getCartContent(user_id)

    if(code == 0):

        user = UserHandler.getUserByID(user_id)

        if cart_contents.__len__() > 0:

            items = list()

            for cart_item in cart_contents:

                item = Items(batch_id = cart_item.batch_id, volume = cart_item.volume)

                items.append(item)

            request = ProcessPaymentRequest(userId = user_id,
                                            amount = cost,
                                            currency = 'EUR',
                                            fiscalAddress = user.address,
                                            items = items,
                                            cardDetails = CardDetails(cardNumber=card_number,
                                                                        cardExpiry=card_expiry,
                                                                        cardCvc=card_cvc)
                                            )
            
            response = client.ProcessPayment(request)

            if(response.response_code == 0):
                #Prepare response

                invoice_id = response.invoiceId
                price = response.invoice.invoice_details.price
                order_id = response.invoice.order_id
                customer_id = response.invoice.customer_id
                fiscal_address = response.invoice.fiscal_address
                details = response.invoice.details

            else:
                # Invalid Order
                response_code = 3

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