import sys

from common.GRPCServer import GRPCServer
from common.GRPCClient import GRPCClient

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

import stubs.store_pb2 as store_pb2
import stubs.store_pb2_grpc as store_pb2_grpc

class Store:
  def __init__(self, server, wallet, account, product_value):
    self.server = server
    self.wallet = wallet
    self.account = account
    self.product_value = product_value
    self.balance = 0
    self.__load_balance()
  
  def Price(self):
    return {
      "price": self.product_value
    }
  
  def Purchase(self, payment_order):
    try:
      transfer = self.wallet.Transfer(value=self.product_value, identifier=payment_order, account=self.account)
      if transfer.result >= 0:
        self.balance += self.product_value
      
      return {
        "value": transfer.result
      }
    except:
      return {
        "value": -9
      }

  def Finish(self):
    self.server.stop(10)
    return {
      "balance": self.balance
    }

  def __load_balance(self):
    self.balance = self.wallet.Balance(identifier=self.account).balance
  
def main(argv):
  product_value = int(argv[1])
  port = int(argv[2])
  account = argv[3]
  wallet_server = argv[4]

  wallet_address = wallet_server.split(":")[0]
  wallet_port = int(wallet_server.split(":")[1])

  wallet_client = GRPCClient(wallet_address, wallet_port)
  Wallet = wallet_client.get_provider("Wallet", wallet_pb2, wallet_pb2_grpc)

  server = GRPCServer()
  server.register(Store, store_pb2, store_pb2_grpc, (server, Wallet, account, product_value))
  server.listen("0.0.0.0", port)

if __name__ == "__main__":
  main(sys.argv)
