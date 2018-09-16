from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from builtins import super
import unittest
import mock
import pytz
from datetime import datetime, timedelta
from parameterized import parameterized
from pprint import pprint
from dpaygo import DPay, exceptions, constants
from dpaygo.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            bundle=False,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )
        cls.appbase = DPay(
            node=nodelist.get_nodes(appbase=True, dev=True),
            nobroadcast=True,
            bundle=False,
            # Overwrite wallet to use this list of wifs only
            keys={"active": wif},
            num_retries=10
        )

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_constants(self, node_param):
        if node_param == "non_appbase":
            stm = self.bts
        else:
            stm = self.appbase
        dpay_conf = stm.get_config()
        if "DPAY_100_PERCENT" in dpay_conf:
            DPAY_100_PERCENT = dpay_conf['DPAY_100_PERCENT']
        else:
            DPAY_100_PERCENT = dpay_conf['DPAY_100_PERCENT']
        self.assertEqual(constants.DPAY_100_PERCENT, DPAY_100_PERCENT)

        if "DPAY_1_PERCENT" in dpay_conf:
            DPAY_1_PERCENT = dpay_conf['DPAY_1_PERCENT']
        else:
            DPAY_1_PERCENT = dpay_conf['DPAY_1_PERCENT']
        self.assertEqual(constants.DPAY_1_PERCENT, DPAY_1_PERCENT)

        if "DPAY_REVERSE_AUCTION_WINDOW_SECONDS" in dpay_conf:
            DPAY_REVERSE_AUCTION_WINDOW_SECONDS = dpay_conf['DPAY_REVERSE_AUCTION_WINDOW_SECONDS']
        else:
            DPAY_REVERSE_AUCTION_WINDOW_SECONDS = dpay_conf['DPAY_REVERSE_AUCTION_WINDOW_SECONDS']
        self.assertEqual(constants.DPAY_REVERSE_AUCTION_WINDOW_SECONDS, DPAY_REVERSE_AUCTION_WINDOW_SECONDS)

        if "DPAY_VOTE_REGENERATION_SECONDS" in dpay_conf:
            DPAY_VOTE_REGENERATION_SECONDS = dpay_conf['DPAY_VOTE_REGENERATION_SECONDS']
        else:
            DPAY_VOTE_REGENERATION_SECONDS = dpay_conf['DPAY_VOTE_REGENERATION_SECONDS']
        self.assertEqual(constants.DPAY_VOTE_REGENERATION_SECONDS, DPAY_VOTE_REGENERATION_SECONDS)

        if "DPAY_ROOT_POST_PARENT" in dpay_conf:
            DPAY_ROOT_POST_PARENT = dpay_conf['DPAY_ROOT_POST_PARENT']
        else:
            DPAY_ROOT_POST_PARENT = dpay_conf['DPAY_ROOT_POST_PARENT']
        self.assertEqual(constants.DPAY_ROOT_POST_PARENT, DPAY_ROOT_POST_PARENT)
