# coding:utf-8
from __future__ import absolute_import, unicode_literals

__author__ = "golden"
__date__ = '2018/1/18'


class Chain(object):
    """ 链结构"""

    def __init__(self, block_cls):
        self.head = None  # 指向最新的block
        self.chain = []
        self.block_cls = block_cls

    def new_block(self, block):
        block = self.block_cls.load(block)
        previous_hash = self.head.hash() if self.head else None
        if self.head == block.index and block.is_valid:
            self.chain.append(block.dict())
