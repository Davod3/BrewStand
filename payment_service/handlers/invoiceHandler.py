# invoiceHandler.py

class InvoiceHandler:
    @staticmethod
    def retrieve_invoice(invoice_id):
        return paymentRepository.retrieve_invoice(invoice_id)

    @staticmethod
    def generate_invoice(user_id, order_id, payment_details):
        # Format and generate invoice details
        invoice_data = {
            'user_id': user_id,
            'order_id': order_id,
            'amount': payment_details['amount'],
            'currency': payment_details['currency'],
            'card_last_four': payment_details['card_last_four']
        }

        paymentRepository.store_invoice(invoice_data)

        return invoice_data
