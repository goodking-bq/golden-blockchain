# coding:utf-8
from __future__ import absolute_import, unicode_literals
import uuid
import time
import hashlib
import json

__author__ = "golden"
__date__ = '2018/1/18'


class Block(object):
    """
    定义区块结构

        magic_no: 魔法数，总是 0xD9B4BEF9
        size: 区块大小,到区块结束的字节长度
        -- header: 区块头 --
            version: 版本
            pre_block: 前一区块的hash,新的区块进来时更新
            time: 时间戳
            merkle_root: 交易的256位hash值，接受交易时更新
            bits: 当前的hash， 挖矿难度调整时更新
            nonce: 随机数
        -- transaction_counter: 交易数量 --
        -- transactions: 交易记录 --
    """

    def __init__(self, data, pre_block=None):
        self.magic_no = 0xD9B4BEF9
        self.index = uuid.uuid4().hex  # 唯一标识
        self.time = int(time.time())  # 时间戳
        self.data = data  # 数据
        self.pre_block = pre_block  # 上一次的
        self.hash = None
        self.transaction_counter = 1
        self.transactions = []
        self.nonce = None
        self.merkle_root = None
        self.version = 1.0

    def __repr__(self):
        return 'Block(%s)' % self.json

    @property
    def dict(self):
        return dict(index=self.index, timestamp=self.timestamp, data=self.data, previous_hash=self.previous_hash,
                    proof=self.proof)

    @property
    def dumps(self):
        return json.dumps(self.dict)

    def loads(self, data):
        d = json.loads(data)
        self.index = d.get('index')
        self.timestamp = d.get('timestamp')
        self.data = d.get('data')
        self.previous_hash = d.get('previous_hash')
        self.proof = d.get('proof')

    def make_hash(self):
        sha512 = hashlib.sha512()
        sha512.update(self.index.encode('utf-8'))
        sha512.update(self.timestamp.encode('utf-8'))
        sha512.update(self.data.encode('utf-8'))
        sha512.update(str(self.previous_hash).encode('utf-8'))
        sha512.update(str(self.proof).encode('utf-8'))
        return sha512.hexdigest()

    def set_proof(self, proof):
        self.proof = proof

    @property
    def is_valid(self):
        self.current_hash = self.make_hash()
        return self.current_hash.endswith('0000')


if __name__ == '__main__':
    b = Block('golden')
    i = 0
    while True:
        b.set_proof(i)
        if b.is_valid:
            break
        i += 1
    print(b)
