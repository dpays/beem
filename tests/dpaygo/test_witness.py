from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from dpaygo import DPay
from dpaygo.witness import Witness, Witnesses, WitnessesVotedByAccount, WitnessesRankedByVote
from dpaygo.instance import set_shared_dpay_instance
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
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        cls.appbase = DPay(
            node=nodelist.get_nodes(normal=False, appbase=True),
            nobroadcast=True,
            unsigned=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_dpay_instance(cls.bts)
        cls.bts.set_default_account("test")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_feed_publish(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        bts.txbuffer.clear()
        w = Witness("gtg", dpay_instance=bts)
        tx = w.feed_publish("4 BBD", "1 BEX")
        self.assertEqual(
            (tx["operations"][0][0]),
            "feed_publish"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["publisher"])

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_update(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        bts.txbuffer.clear()
        w = Witness("gtg", dpay_instance=bts)
        props = {"account_creation_fee": "0.1 BEX",
                 "maximum_block_size": 32000,
                 "bbd_interest_rate": 0}
        tx = w.update(wif, "", props)
        self.assertEqual((tx["operations"][0][0]), "witness_update")
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["owner"])

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_witnesses(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        w = Witnesses(dpay_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_WitnessesVotedByAccount(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        w = WitnessesVotedByAccount("gtg", dpay_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_WitnessesRankedByVote(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        w = WitnessesRankedByVote(dpay_instance=bts)
        w.printAsTable()
        self.assertTrue(len(w) > 0)
        self.assertTrue(isinstance(w[0], Witness))

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_export(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        owner = "gtg"
        if bts.rpc.get_use_appbase():
            witness = bts.rpc.find_witnesses({'owners': [owner]}, api="database")['witnesses']
            if len(witness) > 0:
                witness = witness[0]
        else:
            witness = bts.rpc.get_witness_by_account(owner)

        w = Witness(owner, dpay_instance=bts)
        keys = list(witness.keys())
        json_witness = w.json()
        exclude_list = ['votes', 'virtual_last_update', 'virtual_scheduled_time']
        for k in keys:
            if k not in exclude_list:
                if isinstance(witness[k], dict) and isinstance(json_witness[k], list):
                    self.assertEqual(list(witness[k].values()), json_witness[k])
                else:
                    self.assertEqual(witness[k], json_witness[k])
