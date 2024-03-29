FROM python:3

RUN mkdir /service
RUN mkdir /service/protobufs
COPY ./protobufs/ /service/protobufs
COPY ./order_controller/ /service/

WORKDIR /service/
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/order/order_service.proto

ENTRYPOINT [ "python", "main.py" ]