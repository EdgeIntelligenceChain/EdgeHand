from EdgeHand import EdgeHand


# 初始化钱包,默认本地钱包为mywallet.dat
def sendTxn(txinType=0, addr: str = None, value=110):

    if addr is None:
        # 采取一般方式发送P2PKH交易
        utxo_length = getbalance()
        if utxo_length > 0:
            txn_p2pkh = edgeHand.sendTransaction(txinType, '1NY36FKZqM97oEobfCewhUpHsbzAUSifzo', value)
            txn_status = edgeHand.getTxStatus(txn_p2pkh.id)
            print(txn_status)

    else:
        # 向多签地址发送交易，或发送解锁多签地址的交易（取决于txinType）
        utxo_length = getbalance()
        if utxo_length > 0:
            txn = edgeHand.sendTransaction(txinType, addr, value)
            txn_status = edgeHand.getTxStatus(txn.id)
            print(txn_status)

def getbalance(addr: str = None):
    # 查询钱包余额，当不传入地址时，默认查询初始化钱包的余额
    balance = edgeHand.getBalance4Addr(addr)
    print("balance is : ", end="")
    print(balance)

    utxos = edgeHand.getUTXO4Addr(addr)
    print("the utxo length is : ", end="")
    print(len(utxos))

    return len(utxos)

edgeHand = EdgeHand()

# 地址为空则是默认发送一笔P2PKH交易
# sendTxn()

# 验证多签工作则发送两笔交易
# 产生多签地址
address = edgeHand.getMultiAddress()
print("the P2SH address from keypair is %s" % address)
# # 先向多签地址发送交易
# sendTxn(0, address, 110)
# # 再从多签地址转出，转至随便一个地址
# sendTxn(1, '1NY36FKZqM97oEobfCewhUpHsbzAUSifzo', 20)

# 地址置为空，则表明向
# a = getbalance()
# if a > 0:
#     txn = edgeHand.sendTransaction(0, address, 110)
#     txn_status = edgeHand.getTxStatus(txn.id)
#     print(txn_status)

# b = getbalance(address)
# if b > 0:
#     txn = edgeHand.sendTransaction(1, '1NY36FKZqM97oEobfCewhUpHsbzAUSifzo', 110)
#     txn_status = edgeHand.getTxStatus(txn.id)
#     print(txn_status)

# 发送交易

# print(txn)

#查询交易状态

# 输出样例：
# #185000000000# in address b'1M32gppnnKfCcedHq3weaAagKU7Ppt6KFD'
# #37# utxo in address b'1M32gppnnKfCcedHq3weaAagKU7Ppt6KFD'
# txn 8735269dc5665dea105266ad080a0df003cf3396f9ed296f7f020367f3962ef8 found in_mempool
