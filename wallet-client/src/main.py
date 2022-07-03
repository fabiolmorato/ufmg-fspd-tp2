import grpc
import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

def run():
  with grpc.insecure_channel('localhost:5505') as channel:
    stub = wallet_pb2_grpc.WalletStub(channel)
    response = stub.Balance(wallet_pb2.BalanceParams(identifier="ansbdhas"))
    print("Response: " + str(response.balance))

if __name__ == "__main__":
  run()
