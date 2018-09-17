from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from datetime import datetime, timedelta
import pytz
import time
from pprint import pprint
from dpaygo import DPay
from dpaygo.blockchain import Blockchain
from dpaygo.exceptions import BlockWaitTimeExceeded
from dpaygo.block import Block
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.nodelist import NodeList
from dpaygobase.signedtransactions import Signed_Transaction

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
nodes_appbase = ["https://api.dpays.io", "wss://dpayd.dpays.io", "https://dpaytestapi.com"]


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        cls.appbase = DPay(
            node=nodes_appbase,
            nobroadcast=True,
            keys={"active": wif},
            num_retries=10
        )
        # from getpass import getpass
        # self.bts.wallet.unlock(getpass())
        set_shared_dpay_instance(cls.bts)
        cls.bts.set_default_account("test")

        b = Blockchain(dpay_instance=cls.bts)
        num = b.get_current_block_num()
        cls.start = num - 25
        cls.stop = num

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_blockchain(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        num = b.get_current_block_num()
        self.assertTrue(num > 0)
        self.assertTrue(isinstance(num, int))
        block = b.get_current_block()
        self.assertTrue(isinstance(block, Block))
        self.assertTrue((num - block.identifier) < 3)
        block_time = b.block_time(block.identifier)
        self.assertEqual(block.time(), block_time)
        block_timestamp = b.block_timestamp(block.identifier)
        timestamp = int(time.mktime(block.time().timetuple()))
        self.assertEqual(block_timestamp, timestamp)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_estimate_block_num(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        last_block = b.get_current_block()
        num = last_block.identifier
        old_block = Block(num - 60, dpay_instance=bts)
        date = old_block.time()
        est_block_num = b.get_estimated_block_num(date, accurate=False)
        self.assertTrue((est_block_num - (old_block.identifier)) < 10)
        est_block_num = b.get_estimated_block_num(date, accurate=True)
        self.assertTrue((est_block_num - (old_block.identifier)) < 2)
        est_block_num = b.get_estimated_block_num(date, estimateForwards=True, accurate=True)
        self.assertTrue((est_block_num - (old_block.identifier)) < 2)
        est_block_num = b.get_estimated_block_num(date, estimateForwards=True, accurate=False)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_get_all_accounts(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        accounts = []
        limit = 200
        for acc in b.get_all_accounts(steps=100, limit=limit):
            accounts.append(acc)
        self.assertEqual(len(accounts), limit)
        self.assertEqual(len(set(accounts)), limit)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_awaitTX(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        trans = {'ref_block_num': 3855, 'ref_block_prefix': 1730859721,
                 'expiration': '2018-03-09T06:21:06', 'operations': [],
                 'extensions': [], 'signatures':
                 ['2033a872a8ad33c7d5b946871e4c9cc8f08a5809258355fc909058eac83'
                  '20ac2a872517a52b51522930d93dd2c1d5eb9f90b070f75f838c881ff29b11af98d6a1b']}
        with self.assertRaises(
            Exception
        ):
            b.awaitTxConfirmation(trans)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_stream(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        ops_stream = []
        opNames = ["transfer", "vote"]
        for op in b.stream(opNames=opNames, start=self.start, stop=self.stop):
            ops_stream.append(op)
        self.assertTrue(len(ops_stream) > 0)

        ops_raw_stream = []
        opNames = ["transfer", "vote"]
        for op in b.stream(opNames=opNames, raw_ops=True, start=self.start, stop=self.stop):
            ops_raw_stream.append(op)
        self.assertTrue(len(ops_raw_stream) > 0)

        only_ops_stream = []
        opNames = ["transfer", "vote"]
        for op in b.stream(opNames=opNames, start=self.start, stop=self.stop, only_ops=True):
            only_ops_stream.append(op)
        self.assertTrue(len(only_ops_stream) > 0)

        only_ops_raw_stream = []
        opNames = ["transfer", "vote"]
        for op in b.stream(opNames=opNames, raw_ops=True, start=self.start, stop=self.stop, only_ops=True):
            only_ops_raw_stream.append(op)
        self.assertTrue(len(only_ops_raw_stream) > 0)

        op_stat = b.ops_statistics(start=self.start, stop=self.stop)
        op_stat2 = {"transfer": 0, "vote": 0}
        for op in ops_stream:
            self.assertIn(op["type"], opNames)
            op_stat2[op["type"]] += 1
            self.assertTrue(op["block_num"] >= self.start)
            self.assertTrue(op["block_num"] <= self.stop)
        self.assertEqual(op_stat["transfer"], op_stat2["transfer"])
        self.assertEqual(op_stat["vote"], op_stat2["vote"])

        op_stat3 = {"transfer": 0, "vote": 0}
        for op in ops_raw_stream:
            self.assertIn(op["op"][0], opNames)
            op_stat3[op["op"][0]] += 1
            self.assertTrue(op["block_num"] >= self.start)
            self.assertTrue(op["block_num"] <= self.stop)
        self.assertEqual(op_stat["transfer"], op_stat3["transfer"])
        self.assertEqual(op_stat["vote"], op_stat3["vote"])

        op_stat5 = {"transfer": 0, "vote": 0}
        for op in only_ops_stream:
            self.assertIn(op["type"], opNames)
            op_stat5[op["type"]] += 1
            self.assertTrue(op["block_num"] >= self.start)
            self.assertTrue(op["block_num"] <= self.stop)
        self.assertEqual(op_stat["transfer"], op_stat5["transfer"])
        self.assertEqual(op_stat["vote"], op_stat5["vote"])

        op_stat6 = {"transfer": 0, "vote": 0}
        for op in only_ops_raw_stream:
            self.assertIn(op["op"][0], opNames)
            op_stat6[op["op"][0]] += 1
            self.assertTrue(op["block_num"] >= self.start)
            self.assertTrue(op["block_num"] <= self.stop)
        self.assertEqual(op_stat["transfer"], op_stat6["transfer"])
        self.assertEqual(op_stat["vote"], op_stat6["vote"])

        ops_blocks = []
        for op in b.blocks(start=self.start, stop=self.stop):
            ops_blocks.append(op)
        op_stat4 = {"transfer": 0, "vote": 0}
        self.assertTrue(len(ops_blocks) > 0)
        for block in ops_blocks:
            for tran in block["transactions"]:
                for op in tran['operations']:
                    if isinstance(op, list) and op[0] in opNames:
                        op_stat4[op[0]] += 1
                    elif isinstance(op, dict):
                        op_type = op["type"]
                        if len(op_type) > 10 and op_type[len(op_type) - 10:] == "_operation":
                            op_type = op_type[:-10]
                        if op_type in opNames:
                            op_stat4[op_type] += 1
            self.assertTrue(block.identifier >= self.start)
            self.assertTrue(block.identifier <= self.stop)
        self.assertEqual(op_stat["transfer"], op_stat4["transfer"])
        self.assertEqual(op_stat["vote"], op_stat4["vote"])

        ops_blocks = []
        for op in b.blocks():
            ops_blocks.append(op)
            break
        self.assertTrue(len(ops_blocks) == 1)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_stream2(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts)
        stop_block = b.get_current_block_num()
        start_block = stop_block - 10
        ops_stream = []
        for op in b.stream(start=start_block, stop=stop_block):
            ops_stream.append(op)
        self.assertTrue(len(ops_stream) > 0)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_wait_for_and_get_block(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        b = Blockchain(dpay_instance=bts, max_block_wait_repetition=18)
        start_num = b.get_current_block_num()
        blocknum = start_num
        last_fetched_block_num = None
        for i in range(3):
            block = b.wait_for_and_get_block(blocknum)
            last_fetched_block_num = block.block_num
            blocknum = last_fetched_block_num + 1
        self.assertEqual(last_fetched_block_num, start_num + 2)

        b2 = Blockchain(dpay_instance=bts, max_block_wait_repetition=1)
        with self.assertRaises(
            BlockWaitTimeExceeded
        ):
            for i in range(300):
                block = b2.wait_for_and_get_block(blocknum)
                last_fetched_block_num = block.block_num
                blocknum = last_fetched_block_num + 2

    def test_hash_op(self):
        bts = self.bts
        b = Blockchain(dpay_instance=bts)
        op1 = {'type': 'vote_operation', 'value': {'voter': 'ubg', 'author': 'yesslife', 'permlink': 'dsite-sandwich-contest-week-25-2da-entry', 'weight': 100}}
        op2 = ['vote', {'voter': 'ubg', 'author': 'yesslife', 'permlink': 'dsite-sandwich-contest-week-25-2da-entry', 'weight': 100}]
        hash1 = b.hash_op(op1)
        hash2 = b.hash_op(op2)
        self.assertEqual(hash1, hash2)

    def test_signing_appbase(self):
        b = Blockchain(dpay_instance=self.appbase)
        st = None
        for block in b.blocks(start=25304468, stop=25304468):
            for trx in block.transactions:
                st = Signed_Transaction(trx.copy())
        self.assertTrue(st is not None)
