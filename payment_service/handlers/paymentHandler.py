# paymentHandler.py

class PaymentHandler:
    @staticmethod
    def validate_card_details(card_details):
        if not PaymentHandler.validate_card_number(card_details.card_number):
            return False, "Invalid card number"

        if not PaymentHandler.validate_card_expiry(card_details.card_expiry):
            return False, "Invalid card expiry date"

        if not PaymentHandler.validate_cvc(card_details.card_cvc):
            return False, "Invalid CVC"

        return True
    
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
    def process_payment(user_id, amount, currency, items_id, card_details):
        if not PaymentHandler.validate_card_details(card_details):
            raise ValueError("Invalid card details")

        gateway_response = PaymentHandler.contact_payment_gateway(
            user_id, amount, currency, card_details
        )

        if not gateway_response['success']:
            raise Exception(f"Payment Gateway Error: {gateway_response['message']}")

        card_token = f"token_{gateway_response['transaction_id']}"
        card_last_four = card_details.card_number[-4:]  
        return gateway_response['success'], card_token, card_last_four

