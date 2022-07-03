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
	make __copy_common p=wallet-client
	make __copy_common p=store-server
	make __copy_common p=store-client

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
	rm -rf ./wallet-server/common
	rm -rf ./wallet-client/common
	rm -rf ./store-server/common
	rm -rf ./store-client/common

run_serv_banco:
	make clean > /dev/null
	make stubs > /dev/null
	python3 wallet-server/src/main.py

run_cli_banco:
	make clean > /dev/null
	make stubs > /dev/null
	python3 wallet-client/src/main.py
