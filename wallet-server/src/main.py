from common.GRPCServer import GRPCServer

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

class Wallet:
  def Balance(identifier):
    return {
      "balance": -1
    }

server = GRPCServer()
server.register(Wallet, wallet_pb2, wallet_pb2_grpc)
server.listen('0.0.0.0', '5505')
