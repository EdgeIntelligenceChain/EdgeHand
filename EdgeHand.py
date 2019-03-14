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

logging.basicConfig(
    level=getattr(logging, os.environ.get('TC_LOG_LEVEL', 'INFO')),
    format='[%(asctime)s][%(module)s:%(lineno)d] %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def with_lock(lock):
    def dec(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with lock:
                return func(*args, **kwargs)
        return wrapper
    return dec

class EdgeHand(object):

    def __init__(self, walletFile='mywallet.dat'):

        self.gs = dict()
        self.gs['Block'], self.gs['Transaction'], self.gs['UnspentTxOut'], self.gs['Message'], self.gs['TxIn'], \
            self.gs['TxOut'], self.gs['Peer'] = globals()['Block'], globals()['Transaction'], globals()['UnspentTxOut'],\
                                                globals()['Message'], globals()['TxIn'], globals()['TxOut'], globals()['Peer']

        self.chain_lock = threading.RLock()


        self.wallet = Wallet.init_wallet(walletFile)
        self.peerList = Peer.init_peers(Params.PEERS_FILE)


    def getBalance4Addr(self) -> int:
        with self.chain_lock:
            peer = random.sample(self.peerList, 1)[0]

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(("",0))
            s.listen(1)
            port = s.getsockname()[1]
            s.close()
            message = Message(Actions.Balance4Addr, self.wallet.my_address, port)
            Utils.send_to_peer(message, peer)

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', port))
            s.listen(True)
            conn, addr = s.accept()

            timeout = time.time() + 60
            message = None
            while True and time.time() < timeout:
                if addr[0] == peer[0]:
                    message = Utils.read_all_from_socket(conn, self.gs)
                    if message:
                        break
                else:
                    pass
            conn.close()
            return message.data





