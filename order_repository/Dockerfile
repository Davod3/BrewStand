FROM python:3

RUN mkdir /service
RUN mkdir /service/protobufs
COPY ./protobufs/ /service/protobufs/
COPY ./order_repository/ /service/

WORKDIR /service/
RUN pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/order_repository.proto
        
EXPOSE 50064

ENTRYPOINT [ "python", "main.py" ]