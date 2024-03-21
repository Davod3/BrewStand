FROM python:3

RUN mkdir /service
RUN mkdir /service/protobufs
COPY ./protobufs/ /service/protobufs/
COPY ./api_gateway/ /service/

WORKDIR /service/
RUN pip install -r requirements.txt

# Add a command for each of the required .proto files
RUN python -m grpc_tools.protoc -I ./protobufs --python_out=. \
           --grpc_python_out=. ./protobufs/user.proto

ENTRYPOINT [ "python", "main.py" ]
