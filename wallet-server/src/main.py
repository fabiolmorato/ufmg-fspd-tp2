from common.GRPCServer import GRPCServer

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

class Wallet:
  def __init__(self):
    self.accounts = {}
    self.__load_accounts()

  def __load_accounts(self):
    file = open("contas.txt")
    for line in file:
      data = line.split(" ")
      self.accounts[data[0]] = int(data[1])

  def Balance(self, identifier):
    if not identifier in self.accounts:
      return {
        "balance": -1
      }
    
    return {
      "balance": self.accounts[identifier]
    }
  
  def Stop(self):
    server.stop(0)

server = GRPCServer()
server.register(Wallet, wallet_pb2, wallet_pb2_grpc)
server.listen('0.0.0.0', '5505')
