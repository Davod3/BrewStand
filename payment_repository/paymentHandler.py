from models.invoice import Invoice
from payment_repository_pb2 import InvoiceData  # Import the InvoiceData protobuf

def getInvoice(invoiceId):
    invoice = Invoice.objects.with_id(invoiceId)
    if invoice is None:
        return None

    return InvoiceData(
        invoice_id=invoice.invoice_id,
        price=invoice.price,
        order_id=invoice.order_od,  
        costumer_id=invoice.costumer_id,     
        fiscal_address=invoice.fiscal_address,
        details = invoice.details
    )

def getInvoices(userId):
    invoices = Invoice.objects(userId=userId)
    if not invoices:
        return None

    return [InvoiceData(
        invoice_id=invoice.invoice_id,
        price=invoice.price,
        order_id=invoice.order_od,  
        costumer_id=invoice.costumer_id,     
        fiscal_address=invoice.fiscal_address,
        details = invoice.details
    )for invoice in invoices]
