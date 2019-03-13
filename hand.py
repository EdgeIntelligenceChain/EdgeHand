import binascii
import time
import json
import hashlib
import threading
import _thread
import logging
import socketserver
import socket
import random
import os
from functools import lru_cache, wraps
from typing import (
    Iterable, NamedTuple, Dict, Mapping, Union, get_type_hints, Tuple,
    Callable)
from ds.Transaction import Transaction
from ds.Block  import Block
from ds.UnspentTxOut import UnspentTxOut
from utils.Errors import BlockValidationError
from utils.Utils import Utils

from p2p.Message import Message

from p2p.Peer import Peer
from ds.TxIn import TxIn
from ds.TxOut import TxOut
from ds.MerkleNode import MerkleNode

from p2p.Message import Message
from p2p.Message import Actions

from wallet.Wallet import Wallet
from params.Params import Params

def with_lock(lock):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return dec

gs = dict()
gs['Block'], gs['Transaction'], gs['UnspentTxOut'], gs['Message'], gs['TxIn'], gs['TxOut'], gs['Peer'] = globals()['Block'], \
                    globals()['Transaction'], globals()['UnspentTxOut'], globals()['Message'], \
                    globals()['TxIn'], globals()['TxOut'], globals()['Peer']

chain_lock = threading.RLock()


wallet = Wallet.init_wallet('mywallet.dat')
peerList = Peer.init_peers(Params.PEERS_FILE)

@with_lock(chain_lock)
def getBalance4Addr(addr: str) -> int:
    peer = random.sample(peerList, 1)[0]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    message = Message(Actions.Balance4Addr, addr, port)
    Utils.send_to_peer(message, peer)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(True)
    conn, addr = s.accept()

    timeout = time.time() + 60

    message = None
    while True and time.time() < timeout:
        if addr[0] == peer[0]:
            message = Utils.read_all_from_socket(conn, gs)
            if message:
                break
        else:
            pass
    conn.close()
    return message.data





balance = getBalance4Addr(wallet.my_address)

print('balance is: ', balance)

