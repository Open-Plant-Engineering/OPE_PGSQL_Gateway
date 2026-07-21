python -m grpc_tools.protoc ^
-I proto ^
--python_out=src/gee/grpc/generated ^
--grpc_python_out=src/gee/grpc/generated ^
proto/execution_engine.proto