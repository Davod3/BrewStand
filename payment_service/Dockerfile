FROM python:3

RUN mkdir /service
RUN mkdir /service/protobufs
COPY ./protobufs/ /service/protobufs/
COPY ./payment_service/ /service/

WORKDIR /service/
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/payment/payment_service.proto

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/payment/payment_repository.proto
           
ENTRYPOINT [ "python", "main.py" ]
