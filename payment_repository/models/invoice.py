class Invoice:
    def __init__(self, invoice_details, user_id, order_id, card_last_four):
        self.invoice_details = invoice_details
        self.user_id = user_id
        self.order_id = order_id
        self.card_last_four = card_last_four
