# coding:utf-8
from __future__ import absolute_import, unicode_literals
import os
import hashlib
from binascii import hexlify, unhexlify
import ecdsa
import base58check
import json

__author__ = "golden"
__date__ = '2018/6/22'


class Account(object):
    def __init__(self):
        self.private_key = self.get_private_key()
        self.public_key = self.get_public_key(self.private_key)
        self.address = self.get_address(self.public_key)

    def __repr__(self):
        return "private_key: %s \npublic_key: %s\naddress: %s" % (self.private_key, self.public_key, self.address)

    @classmethod
    def get_private_key(cls):
        """
        对一个随机字符串用 sha256 运算得到一个数字
        :return:
        """
        sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
        sk_string = sk.to_string()
        return hexlify(sk_string)

    @classmethod
    def get_public_key(cls, private_key):
        """
        SECP256k1 运算产生公钥
        :param private_key:
        :return:
        """
        sk = ecdsa.SigningKey.from_string(unhexlify(private_key), curve=ecdsa.SECP256k1)
        vk = sk.get_verifying_key()
        order = ecdsa.SECP256k1.generator.order()
        p = vk.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        y_str = ecdsa.util.number_to_string(p.y(), order)
        compressed = hexlify(bytes(chr(2 + (p.y() & 1)), 'ascii') + x_str).decode('ascii')
        uncompressed = hexlify(bytes(chr(4), 'ascii') + x_str + y_str).decode('ascii')
        return compressed.encode()

    @classmethod
    def get_address(cls, public_key):
        """
        地址是用过 公钥产生，算法是 RIPEMD160(SHA256(K)) ,在经过base58check编码的
        :param public_key:
        :return:
        """
        ripemd160 = hashlib.new('ripemd160', hashlib.sha256(unhexlify(public_key)).digest()).digest()
        data = b'\x00' + ripemd160
        data_2_hash = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]  # 两次hash256取前四个
        data = data + data_2_hash
        result = base58check.b58encode(data)
        return result

    def dumps(self):
        _json = dict(public_key=self.public_key.decode(), address=self.address.decode())
        return json.dumps(_json)

    def dict(self):
        return dict(public_key=self.public_key.decode(), address=self.address.decode())


class AccountManager(object):
    def __init__(self, file='data/account.dat'):
        self.file = file

    def load(self):
        data = json.load(open(self.file))
        return data

    def dump(self, data):
        return json.dump(data, open(self.file, 'w'))

    def add(self):
        a = Account().dict()
        data = self.load()
        data.append(a)
        self.dump(data)
        return a


if __name__ == '__main__':
    print(AccountManager().load())
