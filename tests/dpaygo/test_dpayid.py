from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
from parameterized import parameterized
import random
import json
from pprint import pprint
from dpaygo import DPay, exceptions
from dpaygo.amount import Amount
from dpaygo.memo import Memo
from dpaygo.version import version as dpaygo_version
from dpaygo.wallet import Wallet
from dpaygo.witness import Witness
from dpaygo.account import Account
from dpaygographenebase.account import PrivateKey
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.nodelist import NodeList
from dpaygo.dpayid import DPayId
# Py3 compatibility
import sys
core_unit = "DWB"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)
        cls.appbase = DPay(
            node=nodelist.get_nodes(normal=False, appbase=True),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            num_retries=10)

        cls.account = Account("test", full=True, dpay_instance=cls.bts)
        cls.account_appbase = Account("test", full=True, dpay_instance=cls.appbase)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_transfer(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
            acc = self.account
        elif node_param == "appbase":
            bts = self.appbase
            acc = self.account_appbase
        acc.dpay.txbuffer.clear()
        tx = acc.transfer(
            "test1", 1.000, "BEX", memo="test")
        dpid = DPayId(dpay_instance=bts)
        url = dpid.url_from_tx(tx)
        url_test = 'https://dpayid.io/sign/transfer?from=test&to=test1&amount=1.000+BEX&memo=test'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 4)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 4)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_login_url(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        elif node_param == "appbase":
            bts = self.appbase
        dpid = DPayId(dpay_instance=bts)
        url = dpid.get_login_url("localhost", scope="login,vote")
        url_test = 'https://dpayid.io/oauth2/authorize?client_id=None&redirect_uri=localhost&scope=login,vote'
        self.assertEqual(len(url), len(url_test))
        self.assertEqual(len(url.split('?')), 2)
        self.assertEqual(url.split('?')[0], url_test.split('?')[0])

        url_parts = (url.split('?')[1]).split('&')
        url_test_parts = (url_test.split('?')[1]).split('&')

        self.assertEqual(len(url_parts), 3)
        self.assertEqual(len(list(set(url_parts).intersection(set(url_test_parts)))), 3)
