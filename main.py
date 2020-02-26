from EdgeHand import EdgeHand
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder


# 初始化钱包,默认本地钱包为mywallet.dat
def sendTxn(txinType=0, addr: str = None, value=110):

    if addr is None:
        # 采取一般方式发送P2PKH交易
        utxo_length = getbalance()
        if utxo_length > 0:
            txn_p2pkh = edgeHand.sendTransaction(
                txinType, "1E9HzRbMBVacqSzix5KBMyMxQQLYvhvLA4", value
            )
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

# below annotated lines for test

# this is coinbase author's wallet addr on my machine
# utxos = edgeHand.getUTXO4Addr("1E9HzRbMBVacqSzix5KBMyMxQQLYvhvLA4") 

# this is coinbase tx on my machine
# txid = "7e837eb1ea3643e7c5d64be1c5fce22167534f9fe12f7995b9209bfc35835ce5"

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "world"}


@app.get("/getbalance/{addr}")
def get_balance(addr: str = None):
    balance = edgeHand.getBalance4Addr(addr)
    return {"balance": balance}


@app.get("/getutxo/{addr}")
def get_utxo(addr: str = None):
    """
    return format refers to:
    curl https://blockchain.info/unspent?active=1Cdid9KFAaatwczBwBttQcwXYCpvK8h7FK
    """

    utxos = edgeHand.getUTXO4Addr(addr)
    unspent_outputs = []

    for utxo in utxos:
        utxo_json = {
            "value": utxo.value,
            "to_addr": utxo.to_address,
            "txid": utxo.txid,
            "txout_idx": utxo.txout_idx,
            "is_coinbase": utxo.is_coinbase,
            "htight": utxo.height
        }
        unspent_outputs.append(utxo_json)
    return {"unspent_outputs": unspent_outputs}


@app.get("/gettxstatus/{txid}")
def get_tx_status(txid: str):

    status_msg_map = {
        0: "tx found in mempool",
        1: "tx created by block mined",
        2: "tx not found"
    }

    # note that tx_status is a str, convert it to int
    tx_status = int(edgeHand.getTxStatus(txid))
    return {"tx_status": tx_status, "msg": status_msg_map[tx_status]}


# getbalance()

# 地址为空则是默认发送一笔P2PKH交易
# sendTxn()

# 验证多签工作则发送两笔交易
# 产生多签地址
# address = edgeHand.getMultiAddress()
# print("the P2SH address from keypair is %s" % address)
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

# 查询交易状态

# 输出样例：
# #185000000000# in address b'1M32gppnnKfCcedHq3weaAagKU7Ppt6KFD'
# #37# utxo in address b'1M32gppnnKfCcedHq3weaAagKU7Ppt6KFD'
# txn 8735269dc5665dea105266ad080a0df003cf3396f9ed296f7f020367f3962ef8 found in_mempool
