from EdgeHand import EdgeHand

edgeHand = EdgeHand()
balance = edgeHand.getBalance4Addr()
if balance is not None:
    print('balance is: ', balance)
else:
    print('Exception occurred, and got balance of None')
