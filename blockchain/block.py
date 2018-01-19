# coding:utf-8
from __future__ import absolute_import, unicode_literals
import uuid
import time
import hashlib
import json

__author__ = "golden"
__date__ = '2018/1/18'


class Block(object):
    """定义块结构"""

    def __init__(self, data, previous_hash=None):
        self.index = uuid.uuid4().hex  # 唯一标识
        self.timestamp = str(time.time())  # 时间戳
        self.data = data  # 数据
        self.previous_hash = previous_hash  # 上一次的
        self.proof = None
        self.current_hash = None

    def __repr__(self):
        return 'Block(%s)' % self.json

    @property
    def dict(self):
        return dict(index=self.index, timestamp=self.timestamp, data=self.data, previous_hash=self.previous_hash,
                    proof=self.proof)

    @property
    def json(self):
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
