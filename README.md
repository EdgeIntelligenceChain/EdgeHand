# EdgeHand

Client of Edgence

## API usage

Use [FastAPI](https://github.com/tiangolo/fastapi) to open APIs. Require Python 3.6 or above. 

A quick start:

You need to run [EdgenceChain](https://github.com/EdgeIntelligenceChain/EdgenceChain) first.

```bash
$ python3.6 -m venv venv
$ ./venv/bin/pip3 install -r requirements.txt
$ uvicorn main:app --reload
```

Access `http://127.0.0.1:8000/docs` to see more info about APIs.

## API 简介

所有接口的返回值类型都为 json。接口的请求参数可以在 FastAPI 服务运行之后，参考 `http://127.0.0.1:8000/docs` 中的请求格式。 

### `/getbalance/{addr}`

查询给定钱包的余额。

- 传入参数 `addr` 为钱包地址。

- 返回值为 `{"balance": balance}`。

- 若传入地址不存在，返回余额为 0.

### `/getutxo/{addr}`

查询给定钱包的 utxo。

- 传入参数 `{addr}` 为钱包地址。

- 返回值为该地址对应的 utxo 集合 `{"unspent_outputs": unspent_outputs}` 例如：

```json
{
  "unspent_outputs": [
    {
      "value": 5000000000,
      "to_addr": "76a9283930326232353365313938356665353330613662616139623032346631353132616663336365653288ac",
      "txid": "7e837eb1ea3643e7c5d64be1c5fce22167534f9fe12f7995b9209bfc35835ce5",
      "txout_idx": 0,
      "is_coinbase": true,
      "htight": 2
    },
    {
      "value": 5000000000,
      "to_addr": "76a9283930326232353365313938356665353330613662616139623032346631353132616663336365653288ac",
      "txid": "9ac0b76ae3b096bb47c15158648790b5103dbb818056833ff8370cc5d72294ed",
      "txout_idx": 0,
      "is_coinbase": true,
      "htight": 3
    }
  ]
}
```

### `/gettxstatus/{txid}`

查询给定交易的状态。交易分为三个状态码，表示查询交易的信息：

```
0: "tx found in mempool"
1: "tx created by block mined"
2: "tx not found"
```

- 传入参数 `txid` 为交易 id。

- 返回值为交易的状态码和提示信息，例如：

```json
{
  "tx_status": 1,
  "msg": "tx created by block mined"
}
```

### `/getblockstats`

查询当前链上区块的信息。无输入参数。

- 返回值为当前区块高度 `height`，当前挖矿难度 `difficulity`，当前交易池中的交易数量 `tx_pool_size`，例如：

```json
{
  "height": 5,
  "difficulity": "0.056",
  "tx_pool_size": 0
}
```

### `/getblockheight`

获得当前区块链的高度，数值等同于 `/gatblockstats` 接口返回值的 `height` 字段。为了查询简洁单独做一个请求。

- 无传入参数。

- 返回值为当前区块的高度 `{"height": height}`

### `/getblockinfo/{block_height}`

获得给定区块高度上区块的信息。

- 输入参数为 `block_height` 区块高度。

- 返回值为一个 json。若查询范围不合理，返回值只有 `msg` 字段，值为 `Invalid block height request`。否则返回值如下：

```json
{
  "msg": "Block height valid",
  "height": 3,
  "timestamp": 1582772444,
  "hash": "000000fa375b2910723d612f95c2bcaa3b6aa282ebacd18ebde0586f6643262b",
  "txns": [
    "9ac0b76ae3b096bb47c15158648790b5103dbb818056833ff8370cc5d72294ed"
  ]
}
```

需要注意的是：`txns` 字段是一个 list，表示当前区块包含的所有交易，

### `/getblocksrange`

获得一个给定范围的区块信息。可用于请求所有的区块，或者区块数量多时的分页请求。

- 传入参数为一个范围，`[lower, upper)`。请求地址格式示例：`http://127.0.0.1:8000/getblocksrange?lower=1&upper=3`

- 返回值为 json。若范围不合理，返回值只有 `msg` 字段，值为 `Invalid block range [lower, upper)`。否则返回值如下：

```json
{
  "msg": "Block range valid",
  "blocks": [
    {
      "msg": "Block height valid",
      "height": 1,
      "timestamp": 1554460209,
      "hash": "0000002bfe3135e4b84489d05593cfb8e349ab45e07c49bbb0b2ac2a24bdfed6",
      "txns": [
        "94eceb4186f815410537f69d8c3c70735f661e4ac1a41407564f657aa4201b7f"
      ]
    },
    {
      "msg": "Block height valid",
      "height": 2,
      "timestamp": 1582713977,
      "hash": "0000007317d45cb0eff2c87a91dc51aebc7f47f5f384077375c2e8ce8e68d910",
      "txns": [
        "7e837eb1ea3643e7c5d64be1c5fce22167534f9fe12f7995b9209bfc35835ce5"
      ]
    }
  ]
}
```
