from models.invoice import Invoice
from payment_repository_pb2 import InvoiceData, UserInvoicesResponse 

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
        address=invoice.fiscal_address,
        details = invoice.details
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