FROM python:3

RUN mkdir /service
RUN mkdir /service/protobufs
COPY ./protobufs/ /service/protobufs/
COPY ./payment_controller/ /service/

WORKDIR /service/
RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/payment_service.proto

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/payment_repository.proto

RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/user_service.proto

EXPOSE 3005

ENTRYPOINT [ "python", "main.py" ]
