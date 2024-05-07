# Exporte os segredos para variáveis de ambiente
export INVENTORY_DB_PASSWORD=$(gcloud secrets versions access latest --secret="Inventory_db")
export ORDER_DB_PASSWORD=$(gcloud secrets versions access latest --secret="Order_db")
export PAYMENT_ORDER_SECRET=$(gcloud secrets versions access latest --secret="Payment_order")
export USER_DB_PASSWORD=$(gcloud secrets versions access latest --secret="User_db")


docker compose up --build -d