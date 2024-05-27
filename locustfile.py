from locust import HttpUser, task, between
import json

class BrewstandUser(HttpUser):
    wait_time = between(1,5)

    @task
    def view_items(self):
        response = self.client.get("inventory-api/items")

    @task
    def view_item(self):
        response = self.client.get('inventory-api/items/8114651')
    
    @task
    def view_orders(self):
        response = self.client.get('order-api/order')

    @task
    def view_order(self):
        response = self.client.get('order-api/order/664d17d3f944bcdd40294ec5')
    
    @task
    def view_payments(self):
        response = self.client.get('payment-api/billing')
    
    @task
    def view_payment(self):
        response = self.client.get('payment-api/billing/664d17d304f159705ff01d87')

    @task
    def add_review(self):
        response = self.client.put('review-api/items/8114651/review', data=json.dumps({"score": 7.8}))

    @task
    def buy_item(self):
        
        #Add item to cart
        response = self.client.put('user-api/user/cart', data=json.dumps({"batchID": 8114651,"volume": 1}), name='buy_test')
        
        #Checkout
        response = self.client.post('user-api/user/cart/payment', data=json.dumps({"cardCvc": "007","cardExpiry": "05/24","cardNumber": "123456"}), name='buy_test')


    def on_start(self):
        self.client.headers = {'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFhOHdVMXJIM2tPOFg4TFdnNWhhZCJ9.eyJpc3MiOiJodHRwczovL2Rldi1nY3I3ajMzb2UzbGttMmY0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJCeHl1MHpSYUhMczVYTUZ0Nnh1U1ZYUloxYnI1UzlIdkBjbGllbnRzIiwiYXVkIjoiaHR0cDovL2JyZXdzdGFuZC1hcGkvIiwiaWF0IjoxNzE2MzI2OTIzLCJleHAiOjE3MTg5MTg5MjMsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsImF6cCI6IkJ4eXUwelJhSExzNVhNRnQ2eHVTVlhSWjFicjVTOUh2In0.DTRx8vFjP_hB4lUd3HOTYN4vou9wNvuefeaCiUPy2bp0ZMOoe8j8eCdgR07kwrxctwc_dG6EmIxPlS4PHPuDCyWp0mpQBB_UfHBrQFyZkiWN7LD5kuZKwLno5bNwp5neWxAtHMW4ZRKwcj3mOIUstWHL_uSbjc4CZDw3rZrlmiIKsxG1rM8DnBJlc6I_eLtxvZJAD9HNmlOtlkf4ovozhu5Ki8B8uX-JqDj8VPQIs6WfHoTqdblu8mOA3gW8Rq0RZtQ1MyXcLjI1foBJLyXkZASNOcj1MWscEoxf6eRwcGrNiEOnlDUlKTetcv89sL5OdzSE3GoXnWMY1wlZKVSftA',
                                'Content-type':'application/json'}

