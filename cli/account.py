# coding:utf-8
from __future__ import absolute_import, unicode_literals
import click
from blockchain.account import AccountManager
import json

__author__ = "golden"
__date__ = '2018/6/22'


@click.group(help="account manager")
def account():
    pass


@account.command()
def create():
    """create a count"""
    am = AccountManager()
    click.echo(am.add())


@account.command()
def list():
    """list all account"""
    am = AccountManager()
    data = am.load()
    click.echo(json.dumps(data, indent=4))
