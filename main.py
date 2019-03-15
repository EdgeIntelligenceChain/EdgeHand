from EdgeHand import EdgeHand

edgeHand = EdgeHand()
balance = edgeHand.getBalance4Addr()

print('balance is: ', balance)
result = edgeHand.sendTransaction('1BZG4Tq1XgiJtUEBcnP9UUa7zjmfVuZiQa', 110)
print('sendTransaction result: ', result)
