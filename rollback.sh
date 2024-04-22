kubectl rollout undo deploy/user-controller
kubectl rollout undo deploy/user-service
kubectl rollout undo deploy/user-repository

kubectl rollout undo deploy/inventory-controller
kubectl rollout undo deploy/inventory-service
kubectl rollout undo deploy/inventory-repository

kubectl rollout undo deploy/order-controller
kubectl rollout undo deploy/order-service
kubectl rollout undo deploy/order-repository

kubectl rollout undo deploy/payment-controller
kubectl rollout undo deploy/payment-service
kubectl rollout undo deploy/payment-repository

kubectl rollout undo deploy/review-controller
kubectl rollout undo deploy/review-service
