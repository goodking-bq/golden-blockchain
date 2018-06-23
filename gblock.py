# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from cli import account
import sys
__author__ = "golden"
__date__ = '2018/6/22'


@click.group()
def cli():
    pass


if __name__ == '__main__':
    # sys.argv.append('account')
    # sys.argv.append('list')
    cli.add_command(account)
    cli()
