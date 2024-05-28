from locust import HttpUser, task, between
import json

class BrewstandUser(HttpUser):
    wait_time = between(1,5)

    @task
    def view_items(self):
        response = self.client.get("inventory-api/items")

    @task
    def view_item(self):
        response = self.client.get('inventory-api/items/6441292')
    
    @task
    def view_orders(self):
        response = self.client.get('order-api/order')

    @task
    def view_order(self):
        response = self.client.get('order-api/order/66563d83529b7c55e9eca984')
    
    @task
    def view_payments(self):
        response = self.client.get('payment-api/billing')
    
    @task
    def view_payment(self):
        response = self.client.get('payment-api/billing/66563d83da2b07a19912c2d9')

    @task
    def add_review(self):
        response = self.client.put('review-api/items/6441292/review', data=json.dumps({"score": 7.8}))

    @task
    def buy_item(self):
        
        #Add item to cart
        response = self.client.put('user-api/user/cart', data=json.dumps({"batchID": 6441292,"volume": 0.1}))
        
        #Checkout
        response = self.client.post('user-api/user/cart/payment', data=json.dumps({"cardCvc": "007","cardExpiry": "05/24","cardNumber": "123456"}))


    def on_start(self):
        self.client.headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFhOHdVMXJIM2tPOFg4TFdnNWhhZCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nY3I3ajMzb2UzbGttMmY0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJCeHl1MHpSYUhMczVYTUZ0Nnh1U1ZYUloxYnI1UzlIdkBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2JyZXdzdGFuZC1hcGkvIiwiaWF0IjoxNzE2OTI3NTExLCJleHAiOjE3MTk1MTk1MTEsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkJ4eXUwelJhSExzNVhNRnQ2eHVTVlhSWjFicjVTOUh2In0.pj0r5ZceTxFcP5xeaFGUc1MqjFt4crCnJ0wA5Ab3iAVWtGBNbPMAa76JnqoJY9RwpJkEEtSVep9oyUVapydhKwoQt3Hd00LTcjq7InZh0PLdnXdGYQW9m0lrNh2Lvc-o-ZqOlhNhbvaRV3Wyf3bKRNieqD3kQJyg-WJBoOmPlSpryVf0CFONim8AmrfmoaPJHQ8MUJAym_Cv3O4-vq39cAIUtH01_cDhojfDZ9RYOiZKJpzNv2yx0TZGOZMBh9h37B63m-hIKVq692mHfr9BUhKmtLgtZwjHeJfEkgbTDoHwi9LmzWy9XnhZ-yzMB9QUX96GfEhZS4wZcYIXi614QQ',
                                'Content-type':'application/json'}

