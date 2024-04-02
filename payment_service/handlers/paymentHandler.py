import os
import grpc
import datetime
import re

# Assuming these are the correct paths for your gRPC generated files
from payment_repository_pb2  import StoreInvoiceRequest, InvoiceData, ProcessPaymentResponse
from payment_repository_pb2_grpc import PaymentRepositoryServiceStub

# Corrected environment variable names
payment_repository_host = os.getenv("PAYMENT_REPOSITORY_HOST", "localhost")
payment_repository_port = os.getenv("PAYMENT_REPOSITORY_PORT", "50065")
payment_repository_channel = grpc.insecure_channel(f"{payment_repository_host}:{payment_repository_port}")

client = PaymentRepositoryServiceStub(payment_repository_channel)

class PaymentHandler:
    @staticmethod
    def validate_card_details(card_details):
        if not PaymentHandler.validate_card_number(card_details.card_number):
            return False, "Invalid card number"

        if not PaymentHandler.validate_card_expiry(card_details.card_expiry):
            return False, "Invalid card expiry date"

        if not PaymentHandler.validate_cvc(card_details.card_cvc):
            return False, "Invalid CVC"

        return True, ""

    @staticmethod
    def validate_card_number(card_number):
        """
        Validates the card number using Luhn's algorithm.
        """
        sum_ = 0
        num_digits = len(card_number)
        odd_even = num_digits & 1

        for count in range(num_digits):
            digit = int(card_number[count])

            if not (count & 1) ^ odd_even:
                digit *= 2
            if digit > 9:
                digit -= 9

            sum_ += digit

        return (sum_ % 10) == 0

    @staticmethod
    def validate_card_expiry(expiry_date):
        """
        Validates that the card expiry date is not in the past.
        """
        try:
            expiry = datetime.datetime.strptime(expiry_date, "%m/%y")
            return expiry > datetime.datetime.now()
        except ValueError:
            return False

    @staticmethod
    def validate_cvc(cvc):
        """
        Validates CVC (assuming 3 or 4 digit CVC code).
        """
        return re.match(r"^\d{3,4}$", cvc) is not None

    @staticmethod
    def contact_payment_gateway(user_id, amount, currency, card_details):
        # Simulate contacting a payment gateway
        # In reality, this would involve making a network request to the payment gateway's API.
        response = {
            'success': True,
            'transaction_id': 'txn12345',
            'message': 'Payment processed successfully'
        }
        return response

    @staticmethod
    def validate_payment(user_id, amount, currency, items_id, fiscal_address, card_details):
        is_valid, error_message = PaymentHandler.validate_card_details(card_details)
        if not is_valid:
            return None, error_message

        gateway_response = PaymentHandler.contact_payment_gateway(
            user_id, amount, currency, card_details
        )

        if not gateway_response['success']:
            return None, gateway_response['message']

        card_last_four = card_details.card_number[-4:]  
        return card_last_four, None

    @staticmethod
    def process_payment(user_id, amount, currency, items_name, fiscal_address, card_details):
        
        # Validar o pagamento e obter os últimos quatro dígitos do cartão
        card_last_four, error_message = PaymentHandler.validate_payment(
            user_id=user_id,
            amount=amount,
            currency=currency,
            items=items,
            fiscal_address=fiscal_address,
            card_details=card_details 
        )

        # Se houver um erro na validação do pagamento, retornar um código de erro
        if not card_last_four:
            return ProcessPaymentResponse(response_code = 2, invoiceId = -1, invoice = None)


        # Assuming order_service_pb2 and order_service_pb2_grpc are imported correctly
        # order_channel = grpc.insecure_channel('order_service_endpoint') 
        # order_stub = order_service_pb2_grpc.OrderServiceStub(order_channel)
        # order_response = order_stub.CreateOrder(...) 
        # if not order_response.success:
        #     return 2  # Example error code
        # order_id = order_response.order_id

        # Placeholder para o ID do pedido até que a integração com o serviço de pedidos esteja completa
        order_id = 1

        # Criar uma string para os itens do pedido
        items_list = []
        for item in items:
            items_list.append(f"{item['batch_id']} ({item['volume']})")
        items_name_string = ", ".join(items_list)

        # Criar uma string para os detalhes da fatura
        details_string = f"Card details: **** **** **** {card_last_four} | Items list:\n{items_name_string}"

        # Criar um objeto InvoiceData
        invoice_data = InvoiceData(
            price=amount,
            orderId=order_id,
            userId=user_id,
            fiscalAddress=fiscal_address,
            details=details_string,
        )

        # Armazenar a fatura no serviço de pagamento_repository
        store_invoice_response = client.StoreInvoice(
            StoreInvoiceRequest(invoice=invoice_data)
        )

        # Se houver um erro ao armazenar a fatura, retornar um código de erro
        if store_invoice_response.response_code != 0:
            return ProcessPaymentResponse(response_code = 2, invoiceId = -1, invoice = None)

        # Retornar o ID da fatura armazenada com sucesso
        return ProcessPaymentResponse(response_code = store_invoice_response.response_code, invoiceId = store_invoice_response.invoiceId, invoice = store_invoice_response.invoice)
