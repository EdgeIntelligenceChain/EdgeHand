import binascii
import hashlib
from math import log

import ecdsa
from base58 import b58encode_check, b58decode_check

from ds import MerkleNode
from ds import Block
from ds import Transaction
from ds import TxIn
from ds import TxOut

from params import Params
from script import scriptBuild

from utils.Utils import Utils

from ds.OutPoint import OutPoint
from ds.TxOut import TxOut

import EdgeHand


def pubkey_to_address(pubkey: bytes) -> str:
    if 'ripemd160' not in hashlib.algorithms_available:
        raise RuntimeError('missing ripemd160 hash algorithm')

    sha = hashlib.sha256(pubkey).digest()
    ripe = hashlib.new('ripemd160', sha).digest()

    address = b58encode_check(b'\x00' + ripe)
    address = address if isinstance(address, str) else str(address, encoding="utf-8")
    return address

def build_spend_message(to_spend, pk, sequence, txouts):

    spend_msg = Utils.sha256d(
        Utils.serialize(to_spend) + str(sequence) +
        binascii.hexlify(pk).decode() + Utils.serialize(txouts)).encode()

    return spend_msg

def check_signature():
    print("---------TEST----------")

    # 产生私钥
    signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    # 产生公钥
    pk = signing_key.get_verifying_key().to_string()

    outpoint = OutPoint(txid='c47852b74825cc2bbd39faafb588b50243de9bb453dd9f48167d12bb360848cc', txout_idx=0)
    txouts=[TxOut(value=110, pk_script=EdgeHand.EdgeHand()._make_pk_script('1NY36FKZqM97oEobfCewhUpHsbzAUSifzo')),
                  TxOut(value=4999999890, pk_script=EdgeHand.EdgeHand()._make_pk_script('1BP9KYivYyhPEbg2WDFTf83i8wnyFYuRGH'))]
    sequence = 0

    data1 = build_spend_message(outpoint, pk, sequence, txouts)

    signature = signing_key.sign(data1)
    print(data1)

    # 获取公钥对应的验证秘钥
    verifying_key = ecdsa.VerifyingKey.from_string(
        pk, curve=ecdsa.SECP256k1)

    # 重新构建秘钥及其验证过程
    tx_copy = build_spend_message(outpoint, pk, sequence, txouts)
    valid = verifying_key.verify(signature, tx_copy)

    print(valid)

    print("---------DONE----------")

    return None

if __name__ == '__main__':

    check_signature()
