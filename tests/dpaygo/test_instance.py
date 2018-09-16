from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
from parameterized import parameterized
from pprint import pprint
from dpaygo import DPay
from dpaygo.amount import Amount
from dpaygo.witness import Witness
from dpaygo.account import Account
from dpaygo.instance import set_shared_dpay_instance, shared_dpay_instance, set_shared_config
from dpaygo.blockchain import Blockchain
from dpaygo.block import Block
from dpaygo.market import Market
from dpaygo.price import Price
from dpaygo.comment import Comment
from dpaygo.vote import Vote
from dpaygoapi.exceptions import RPCConnection
from dpaygo.wallet import Wallet
from dpaygo.transactionbuilder import TransactionBuilder
from dpaygobase.operations import Transfer
from dpaygographenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaygo.utils import parse_time, formatTimedelta
from dpaygo.nodelist import NodeList

# Py3 compatibility
import sys

core_unit = "DWB"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(dpay_instance=DPay(node=cls.nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        stm = DPay(node=cls.nodelist.get_nodes())
        stm.config.refreshBackup()
        stm.set_default_nodes(["xyz"])
        del stm

        cls.urls = cls.nodelist.get_nodes()
        cls.bts = DPay(
            node=cls.urls,
            nobroadcast=True,
            num_retries=10
        )
        set_shared_dpay_instance(cls.bts)
        acc = Account("holger80", dpay_instance=cls.bts)
        comment = acc.get_blog(limit=20)[-1]
        cls.authorperm = comment.authorperm
        votes = acc.get_account_votes()
        last_vote = votes[-1]
        cls.authorpermvoter = '@' + last_vote['authorperm'] + '|' + acc["name"]

    @classmethod
    def tearDownClass(cls):
        stm = DPay(node=cls.nodelist.get_nodes())
        stm.config.recover_with_latest_backup()

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_account(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            acc = Account("test")
            self.assertIn(acc.dpay.rpc.url, self.urls)
            self.assertIn(acc["balance"].dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test", dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            acc = Account("test", dpay_instance=stm)
            self.assertIn(acc.dpay.rpc.url, self.urls)
            self.assertIn(acc["balance"].dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Account("test")

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_amount(self, node_param):
        if node_param == "instance":
            stm = DPay(node="https://abc.d", autoconnect=False, num_retries=1)
            set_shared_dpay_instance(self.bts)
            o = Amount("1 BBD")
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 BBD", dpay_instance=stm)
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Amount("1 BBD", dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Amount("1 BBD")

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_block(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Block(1)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1, dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Block(1, dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Block(1)

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_blockchain(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Blockchain()
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain(dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Blockchain(dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Blockchain()

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_comment(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Comment(self.authorperm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm, dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Comment(self.authorperm, dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Comment(self.authorperm)

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_market(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Market()
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market(dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Market(dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Market()

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_price(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Price(10.0, "BEX/BBD")
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "BEX/BBD", dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Price(10.0, "BEX/BBD", dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Price(10.0, "BEX/BBD")

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_vote(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Vote(self.authorpermvoter)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter, dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Vote(self.authorpermvoter, dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Vote(self.authorpermvoter)

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_wallet(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Wallet()
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet(dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
                o.dpay.get_config()
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Wallet(dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = Wallet()
                o.dpay.get_config()

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_witness(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = Witness("gtg")
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg", dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = Witness("gtg", dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                Witness("gtg")

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_transactionbuilder(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = TransactionBuilder()
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder(dpay_instance=DPay(node="https://abc.d", autoconnect=False, num_retries=1))
                o.dpay.get_config()
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = TransactionBuilder(dpay_instance=stm)
            self.assertIn(o.dpay.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                o = TransactionBuilder()
                o.dpay.get_config()

    @parameterized.expand([
        ("instance"),
        ("dpay")
    ])
    def test_dpay(self, node_param):
        if node_param == "instance":
            set_shared_dpay_instance(self.bts)
            o = DPay(node=self.urls)
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = DPay(node="https://abc.d", autoconnect=False, num_retries=1)
                stm.get_config()
        else:
            set_shared_dpay_instance(DPay(node="https://abc.d", autoconnect=False, num_retries=1))
            stm = self.bts
            o = stm
            o.get_config()
            self.assertIn(o.rpc.url, self.urls)
            with self.assertRaises(
                RPCConnection
            ):
                stm = shared_dpay_instance()
                stm.get_config()

    def test_config(self):
        set_shared_config({"node": self.urls})
        set_shared_dpay_instance(None)
        o = shared_dpay_instance()
        self.assertIn(o.rpc.url, self.urls)
