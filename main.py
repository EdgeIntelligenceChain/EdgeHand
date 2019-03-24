from EdgeHand import EdgeHand

#初始化钱包,默认本地钱包为mywallet.dat
edgeHand = EdgeHand()

#查询钱包余额，当不传入地址时，默认查询初始化钱包的余额
balance = edgeHand.getBalance4Addr()

#发送交易
txn = edgeHand.sendTransaction('1NY36FKZqM97oEobfCewhUpHsbzAUSifzo', 110)

#查询交易状态
edgeHand.getTxStatus(txn)

