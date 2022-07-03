from common.GRPCServer import GRPCServer

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

class Wallet:
  def __init__(self):
    self.accounts = {}
    self.__load_accounts()

  def Balance(self, identifier):
    if not identifier in self.accounts:
      return {
        "balance": -1
      }
    
    return {
      "balance": self.accounts[identifier]
    }
  
  def Stop(self):
    self.__save_accounts()
    server.stop(10)
    return {
      "accounts": len(self.accounts)
    }

  def __load_accounts(self):
    file = open("contas.txt")
    for line in file:
      if line == "":
        continue
      data = line.split(" ")
      self.accounts[data[0]] = int(data[1])
  
  def __save_accounts(self):
    file = open("contas.txt", "w")
    for account in self.accounts:
      file.write(f"{account} {self.accounts[account]}\n")

server = GRPCServer()
server.register(Wallet, wallet_pb2, wallet_pb2_grpc)
server.listen('0.0.0.0', '5505')
