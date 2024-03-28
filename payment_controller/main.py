from flask import Flask, request, jsonify, abort
import grpc
import payment_pb2
import payment_pb2_grpc

app = Flask(__name__)

def get_grpc_stub():
    channel = grpc.insecure_channel('payment_service')
    stub = payment_pb2_grpc.PaymentServiceStub(channel)
    return stub

@app.route('/billing/<int:orderId>', methods=['GET'])
def get_invoice(invoiceId):
    user_id = get_user_id_from_token()  # Extract user ID from token
    stub = get_grpc_stub()
    try:
        response = stub.GetInvoice(payment_pb2.InvoiceRequest(user_id=user_id, invoice_id=orderId))
        return jsonify(response.invoice)
    except grpc.RpcError as e:
        abort(404, "Requested invoice was not found")

@app.route('/billing', methods=['GET'])
def get_invoices():
    user_id = get_user_id_from_token()  # Extract user ID from token
    stub = get_grpc_stub()
    try:
        response = stub.GetAllInvoices(payment_pb2.GetAllInvoicesRequest(user_id))
        return jsonify([invoice for invoice in response.invoices])
    except grpc.RpcError as e:
        abort(404, "Requested invoices were not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
