import sys

from common.GRPCClient import GRPCClient

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

import stubs.store_pb2 as store_pb2
import stubs.store_pb2_grpc as store_pb2_grpc

def main(argv):
  account = argv[1]
  wallet_server = argv[2]
  store_server = argv[3]

  wallet_address = wallet_server.split(":")[0]
  wallet_port = int(wallet_server.split(":")[1])

  store_address = store_server.split(":")[0]
  store_port = int(store_server.split(":")[1])

  wallet_server = GRPCClient(wallet_address, wallet_port)
  store_server = GRPCClient(store_address, store_port)

  Wallet = wallet_server.get_provider("Wallet", wallet_pb2, wallet_pb2_grpc)
  Store = store_server.get_provider("Store", store_pb2, store_pb2_grpc)

  last_price = 0

  while True:
    line = input()
    parts = line.split(" ")
    command = parts[0]

    if command == "P":
      price = Store.Price().price
      balance = Wallet.Balance(identifier=account).balance
      print(f'{price} {balance}')
      last_price = price
    
    elif command == "C":
      payment_order = Wallet.PaymentOrder(identifier=account, value=last_price)
      print(payment_order.status)
      if payment_order.status >= 0:
        purchase = Store.Purchase(payment_order=payment_order.identifier)
        print(purchase.value)
    
    elif command == "T":
      exit = Store.Finish()
      print(exit.balance)
      wallet_exit = Wallet.Stop()
      print(wallet_exit.accounts)
      break

if __name__ == "__main__":
  main(sys.argv)
