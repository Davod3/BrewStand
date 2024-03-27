from flask import Flask, request, jsonify, abort
import grpc
import payment_pb2
import payment_pb2_grpc

app = Flask(__name__)

def get_grpc_stub():
    channel = grpc.insecure_channel('payment_service')
    stub = payment_pb2_grpc.PaymentServiceStub(channel)
    return stub

@app.route('/billing/<int:invoiceId>', methods=['GET'])
def get_invoice(invoiceId):
    stub = get_grpc_stub()
    try:
        response = stub.GetInvoice(payment_pb2.InvoiceRequest(invoice_id=invoiceId))
        return jsonify(response.invoice)
    except grpc.RpcError as e:
        abort(404, "Requested invoice was not found")

@app.route('/billing', methods=['GET'])
def get_invoices():
    stub = get_grpc_stub()
    try:
        response = stub.GetAllInvoices(payment_pb2.GetAllInvoicesRequest())
        return jsonify([invoice for invoice in response.invoices])
    except grpc.RpcError as e:
        abort(404, "Requested invoices were not found")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
