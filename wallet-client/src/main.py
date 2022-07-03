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

  payment_orders = {}
  payment_order_id = 1

  while True:
    line = input()
    parts = line.split(" ")
    command = parts[0]

    if command == "S":
      balance = Wallet.Balance(identifier=identifier).balance
      print(balance)

    elif command == "O":
      value = int(parts[1])
      payment_order = Wallet.PaymentOrder(identifier=identifier, value=value)
      if payment_order.status < 0:
        print(payment_order.status)
        continue
      payment_orders[payment_order_id] = payment_order.identifier
      print(payment_order_id)
      payment_order_id += 1

    elif command == "T":
      value = int(parts[1])
      payment_order = int(parts[2])
      account = parts[3]

      if not payment_order in payment_orders:
        print(-9)
        continue

      identifier = payment_orders[payment_order]
      result = Wallet.Transfer(value=value, identifier=identifier, account=account).result
      print(result)
      del payment_orders[payment_order]

    elif command == "F":
      accounts_saved = Wallet.Stop().accounts
      print(accounts_saved)
      break

if __name__ == "__main__":
  main(sys.argv)
