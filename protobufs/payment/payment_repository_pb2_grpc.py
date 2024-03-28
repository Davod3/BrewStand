# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import payment_repository_pb2 as payment__repository__pb2


class PaymentRepositoryServiceStub(object):
    """The PaymentRepositoryService handles data storage and retrieval for payments and invoices.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StorePayment = channel.unary_unary(
                '/payment_repository.PaymentRepositoryService/StorePayment',
                request_serializer=payment__repository__pb2.PaymentData.SerializeToString,
                response_deserializer=payment__repository__pb2.StorePaymentResponse.FromString,
                )
        self.RetrievePayment = channel.unary_unary(
                '/payment_repository.PaymentRepositoryService/RetrievePayment',
                request_serializer=payment__repository__pb2.PaymentQuery.SerializeToString,
                response_deserializer=payment__repository__pb2.PaymentData.FromString,
                )
        self.StoreInvoice = channel.unary_unary(
                '/payment_repository.PaymentRepositoryService/StoreInvoice',
                request_serializer=payment__repository__pb2.InvoiceData.SerializeToString,
                response_deserializer=payment__repository__pb2.StoreInvoiceResponse.FromString,
                )
        self.RetrieveInvoice = channel.unary_unary(
                '/payment_repository.PaymentRepositoryService/RetrieveInvoice',
                request_serializer=payment__repository__pb2.InvoiceQuery.SerializeToString,
                response_deserializer=payment__repository__pb2.InvoiceData.FromString,
                )


class PaymentRepositoryServiceServicer(object):
    """The PaymentRepositoryService handles data storage and retrieval for payments and invoices.
    """

    def StorePayment(self, request, context):
        """Stores payment details.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrievePayment(self, request, context):
        """Retrieves payment details.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StoreInvoice(self, request, context):
        """Stores invoice details.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RetrieveInvoice(self, request, context):
        """Retrieves invoice details.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_PaymentRepositoryServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StorePayment': grpc.unary_unary_rpc_method_handler(
                    servicer.StorePayment,
                    request_deserializer=payment__repository__pb2.PaymentData.FromString,
                    response_serializer=payment__repository__pb2.StorePaymentResponse.SerializeToString,
            ),
            'RetrievePayment': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrievePayment,
                    request_deserializer=payment__repository__pb2.PaymentQuery.FromString,
                    response_serializer=payment__repository__pb2.PaymentData.SerializeToString,
            ),
            'StoreInvoice': grpc.unary_unary_rpc_method_handler(
                    servicer.StoreInvoice,
                    request_deserializer=payment__repository__pb2.InvoiceData.FromString,
                    response_serializer=payment__repository__pb2.StoreInvoiceResponse.SerializeToString,
            ),
            'RetrieveInvoice': grpc.unary_unary_rpc_method_handler(
                    servicer.RetrieveInvoice,
                    request_deserializer=payment__repository__pb2.InvoiceQuery.FromString,
                    response_serializer=payment__repository__pb2.InvoiceData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'payment_repository.PaymentRepositoryService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class PaymentRepositoryService(object):
    """The PaymentRepositoryService handles data storage and retrieval for payments and invoices.
    """

    @staticmethod
    def StorePayment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_repository.PaymentRepositoryService/StorePayment',
            payment__repository__pb2.PaymentData.SerializeToString,
            payment__repository__pb2.StorePaymentResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrievePayment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_repository.PaymentRepositoryService/RetrievePayment',
            payment__repository__pb2.PaymentQuery.SerializeToString,
            payment__repository__pb2.PaymentData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StoreInvoice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_repository.PaymentRepositoryService/StoreInvoice',
            payment__repository__pb2.InvoiceData.SerializeToString,
            payment__repository__pb2.StoreInvoiceResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RetrieveInvoice(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/payment_repository.PaymentRepositoryService/RetrieveInvoice',
            payment__repository__pb2.InvoiceQuery.SerializeToString,
            payment__repository__pb2.InvoiceData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)