from models.invoice import Invoice
from payment_repository_pb2 import InvoiceData, UserInvoicesResponse 

def getInvoice(invoiceId):
    invoice = Invoice.objects.with_id(invoiceId)
    if invoice is None:
        return None

    return Invoice(
        invoice_id=invoice.invoice_id,
        price=invoice.price,
        order_id=invoice.order_id,  
        customer_id=invoice.customer_id,     
        fiscal_address=invoice.fiscal_address,
        details=invoice.details
    )

def getInvoices(userId):
    try:
        invoices = Invoice.objects(userId=userId)

        if invoices is None:
             return UserInvoicesResponse(content=None)
        else:
            converted_invoices = [convertToRPC(invoice) for invoice in invoices]
            return UserInvoicesResponse(content=converted_invoices)
        
    except Exception as e:
        return UserInvoicesResponse(content=None)