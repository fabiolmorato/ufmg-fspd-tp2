stubs:
	mkdir -p ./stubs/stubs
	python3 -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/stubs/*.proto
	make copy

copy:
	make __copy_stubs p=wallet-server
	make __copy_stubs p=wallet-client
	make __copy_stubs p=store-server
	make __copy_stubs p=store-client
	make __copy_common p=wallet-server

__copy_stubs:
	mkdir -p $(p)/src/stubs
	cp -r stubs/* $(p)/src/stubs

__copy_common:
	mkdir -p $(p)/src/common
	cp -r common/* $(p)/src/common

clean:
	rm -rf ./wallet-server/src/stubs
	rm -rf ./wallet-client/src/stubs
	rm -rf ./store-server/src/stubs
	rm -rf ./store-client/src/stubs
	rm -rf stubs

run_serv_banco:
	python3 wallet-server/src/main.py

run_cli_banco:
	python3 wallet-client/src/main.py