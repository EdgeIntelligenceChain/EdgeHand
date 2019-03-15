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

from utils.Utils import Utils
from utils.Errors import BaseException, Parse2MessageError, PortGenerateError, ListenError, UnwantedResultError

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

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(("",0))
                s.listen(1)
                port = s.getsockname()[1]
                s.close()
                message = Message(Actions.Balance4Addr, self.wallet.my_address, port)
                returnSend = Utils.send_to_peer(message, peer)
            except Exception:
                logger.info(f'cannot generate a random port or some Exception ofsend Balance4Arr message')
                return None
            else:
                if returnSend is False:
                    logger.info('Utils.send_to_peer returns False')
                    return None



            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.bind(('', port))
                s.listen(True)
                conn, addr = s.accept()
            except Exception:
                logger.exception('listening thread cannot be established successfully')
                return None

            timeout = time.time() + 60
            message = None
            while True and time.time() < timeout:
                if addr[0] == peer[0]:
                    try:
                        message = Utils.read_all_from_socket(conn, self.gs)
                        if message:
                            break
                    except Exception:
                        logger.exception('cannot parse the obtained data into  a Message object')
                        return None
            try:
                conn.close()
            except Exception:
                logger.exception('network connection cannot be closed')
                return None
            if not isinstance(message.data, int):
                logger.info('message.data is not an int object, which cannot be a balance')
                return None

            return message.data





