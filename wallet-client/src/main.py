from common.GRPCClient import GRPCClient

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

client = GRPCClient("0.0.0.0", 5505)
Wallet = client.get_provider("Wallet", wallet_pb2, wallet_pb2_grpc)
print(Wallet.Balance(identifier="asbdfhsbh"))
