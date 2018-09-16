from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from dpaygo import DPay, exceptions
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.account import Account
from dpaygo.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        cls.bts = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_dpay_instance(cls.bts)

    def test_get_nodes(self):
        nodelist = NodeList()
        all_nodes = nodelist.get_nodes(normal=True, appbase=True, dev=True, testnet=True, testnetdev=True)
        self.assertEqual(len(nodelist) - 6, len(all_nodes))
        https_nodes = nodelist.get_nodes(wss=False)
        self.assertEqual(https_nodes[0][:5], 'https')

    def test_nodes_update(self):
        nodelist = NodeList()
        all_nodes = nodelist.get_nodes(normal=True, appbase=True, dev=True, testnet=True)
        nodelist.update_nodes(dpay_instance=self.bts)
        nodes = nodelist.get_nodes()
        self.assertIn(nodes[0], all_nodes)
