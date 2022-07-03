import sys

from common.GRPCClient import GRPCClient

import stubs.wallet_pb2 as wallet_pb2
import stubs.wallet_pb2_grpc as wallet_pb2_grpc

def main(argv):
  identifier = argv[1]
  server = argv[2]

  address = server.split(":")[0]
  port = int(server.split(":")[1])

  client = GRPCClient(address, port)
  Wallet = client.get_provider("Wallet", wallet_pb2, wallet_pb2_grpc)

  while True:
    line = input()
    parts = line.split(" ")
    command = parts[0]

    payment_orders = {}
    payment_order_id = 1

    if command == "S":
      balance = Wallet.Balance(identifier=identifier).balance
      print(balance)
    elif command == "O":
      value = int(parts[1])
      payment_order = Wallet.PaymentOrder(identifier=identifier, value=value)
      print(payment_order.status)
      payment_orders[payment_order_id] = payment_order.identifier
      payment_order_id += 1
    elif command == "F":
      accounts_saved = Wallet.Stop().accounts
      print(accounts_saved)
      break

if __name__ == "__main__":
  main(sys.argv)
