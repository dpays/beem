import unittest
from dpaygo import DPay
from dpaygo.account import Account
from dpaygo.instance import set_shared_dpay_instance, SharedInstance
from dpaygo.blockchainobject import BlockchainObject
from dpaygo.nodelist import NodeList

import logging
log = logging.getLogger()


class Testcases(unittest.TestCase):

    def test_stm1stm2(self):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        b1 = DPay(
            node=nodelist.get_testnet(testnet=True, testnetdev=False),
            nobroadcast=True,
            num_retries=10
        )

        b2 = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            num_retries=10
        )

        self.assertNotEqual(b1.rpc.url, b2.rpc.url)

    def test_default_connection(self):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        b1 = DPay(
            node=nodelist.get_testnet(testnet=True, testnetdev=False),
            nobroadcast=True,
        )
        set_shared_dpay_instance(b1)
        test = Account("dpaygo")

        b2 = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
        )
        set_shared_dpay_instance(b2)

        bts = Account("dpaygo")

        self.assertEqual(test.dpay.prefix, "DWT")
        self.assertEqual(bts.dpay.prefix, "DWB")
