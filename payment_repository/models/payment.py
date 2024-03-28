class Payment:
    def __init__(self, user_id, amount, currency, items_id, card_token, card_last_four):
        self.user_id = user_id
        self.amount = amount
        self.currency = currency
        self.items_id = items_id
        self.card_token = card_token
        self.card_last_four = card_last_four
