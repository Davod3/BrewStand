from models.invoice import Invoice
from payment_repository_pb2 import InvoiceData  # Import the InvoiceData protobuf

def getInvoice(invoiceId):
    invoice = Invoice.objects.with_id(invoiceId)
    if invoice is None:
        return None

    return InvoiceData(
        invoiceId=str(invoice.id),
        price=invoice.price,
        orderID=invoice.orderID,  
        userId=invoice.userId,     
        fiscalAddress=invoice.fiscalAddress,
        cardLastFour=invoice.cardLastFour,
        items_name=invoice.items_name  
    )

def getInvoices(userId):
    invoices = Invoice.objects(userId=userId)
    if not invoices:
        return None

    return [InvoiceData(
        invoiceId=str(inv.id),
        price=inv.price,
        orderID=str(inv.orderID),
        userId=str(inv.userId),
        fiscalAddress=inv.fiscalAddress,
        cardLastFour=inv.cardLastFour,
        items_name=inv.items_name
    ) for inv in invoices]
