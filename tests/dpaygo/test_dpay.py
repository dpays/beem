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
# Py3 compatibility
import sys
core_unit = "DWB"
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nodelist = NodeList()
        cls.nodelist.update_nodes(dpay_instance=DPay(node=cls.nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.bts = DPay(
            node=cls.nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10)
        cls.appbase = DPay(
            node=cls.nodelist.get_nodes(normal=False, appbase=True),
            nobroadcast=True,
            unsigned=True,
            data_refresh_time_seconds=900,
            keys={"active": wif, "owner": wif, "memo": wif},
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
            "test", 1.33, "BBD", memo="Foobar", account="test1")
        self.assertEqual(
            tx["operations"][0][0],
            "transfer"
        )
        self.assertEqual(len(tx["operations"]), 1)
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertEqual(op["memo"], "Foobar")
        self.assertEqual(op["from"], "test1")
        self.assertEqual(op["to"], "test")
        amount = Amount(op["amount"], dpay_instance=bts)
        self.assertEqual(float(amount), 1.33)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_create_account(self, node_param):
        if node_param == "non_appbase":
            bts = DPay(node=self.nodelist.get_nodes(appbase=False),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        elif node_param == "appbase":
            bts = DPay(node=self.nodelist.get_nodes(normal=False, appbase=True),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        key5 = PrivateKey()
        bts.txbuffer.clear()
        tx = bts.create_account(
            name,
            creator="test",   # 1.2.7
            owner_key=format(key1.pubkey, core_unit),
            active_key=format(key2.pubkey, core_unit),
            posting_key=format(key3.pubkey, core_unit),
            memo_key=format(key4.pubkey, core_unit),
            additional_owner_keys=[format(key5.pubkey, core_unit)],
            additional_active_keys=[format(key5.pubkey, core_unit)],
            additional_posting_keys=[format(key5.pubkey, core_unit)],
            additional_owner_accounts=["test1"],  # 1.2.0
            additional_active_accounts=["test1"],
            storekeys=False,
            delegation_fee_dpay="0 BEX"
        )
        self.assertEqual(
            tx["operations"][0][0],
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        role = "posting"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["creator"],
            "test")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_create_account_password(self, node_param):
        if node_param == "non_appbase":
            bts = DPay(node=self.nodelist.get_nodes(appbase=False),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        elif node_param == "appbase":
            bts = DPay(node=self.nodelist.get_nodes(normal=False, appbase=True),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key5 = PrivateKey()
        bts.txbuffer.clear()
        tx = bts.create_account(
            name,
            creator="test",   # 1.2.7
            password="abcdefg",
            additional_owner_keys=[format(key5.pubkey, core_unit)],
            additional_active_keys=[format(key5.pubkey, core_unit)],
            additional_posting_keys=[format(key5.pubkey, core_unit)],
            additional_owner_accounts=["test1"],  # 1.2.0
            additional_active_accounts=["test1"],
            storekeys=False,
            delegation_fee_dpay="0 BEX"
        )
        self.assertEqual(
            tx["operations"][0][0],
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["creator"],
            "test")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_create_account_with_delegation(self, node_param):
        if node_param == "non_appbase":
            bts = DPay(node=self.nodelist.get_nodes(appbase=False),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        elif node_param == "appbase":
            bts = DPay(node=self.nodelist.get_nodes(normal=False, appbase=True),
                        nobroadcast=True,
                        unsigned=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        key5 = PrivateKey()
        bts.txbuffer.clear()
        tx = bts.create_account(
            name,
            creator="test",   # 1.2.7
            owner_key=format(key1.pubkey, core_unit),
            active_key=format(key2.pubkey, core_unit),
            posting_key=format(key3.pubkey, core_unit),
            memo_key=format(key4.pubkey, core_unit),
            additional_owner_keys=[format(key5.pubkey, core_unit)],
            additional_active_keys=[format(key5.pubkey, core_unit)],
            additional_owner_accounts=["test1"],  # 1.2.0
            additional_active_accounts=["test1"],
            storekeys=False,
            delegation_fee_dpay="1 BEX"
        )
        self.assertEqual(
            tx["operations"][0][0],
            "account_create_with_delegation"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            format(key5.pubkey, core_unit),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "test1",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["creator"],
            "test")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_connect(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        elif node_param == "appbase":
            bts = self.appbase
        bts.connect()

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_info(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        elif node_param == "appbase":
            bts = self.appbase
        info = bts.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'current_witness',
                    'total_pow',
                    'time']:
            self.assertTrue(key in info)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_finalizeOps(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
            acc = self.account
        elif node_param == "appbase":
            bts = self.appbase
            acc = self.account_appbase
        tx1 = bts.new_tx()
        tx2 = bts.new_tx()

        acc.transfer("test1", 1, "BEX", append_to=tx1)
        acc.transfer("test1", 2, "BEX", append_to=tx2)
        acc.transfer("test1", 3, "BEX", append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_weight_threshold(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        elif node_param == "appbase":
            bts = self.appbase

        auth = {'account_auths': [['test', 1]],
                'extensions': [],
                'key_auths': [
                    ['DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['DWB7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 3}  # threshold fine
        bts._test_weights_treshold(auth)
        auth = {'account_auths': [['test', 1]],
                'extensions': [],
                'key_auths': [
                    ['DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['DWB7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 4}  # too high

        with self.assertRaises(ValueError):
            bts._test_weights_treshold(auth)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_allow(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
            acc = self.account
        elif node_param == "appbase":
            bts = self.appbase
            acc = self.account_appbase
        self.assertIn(bts.prefix, "DWB")
        tx = acc.allow(
            "DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
            account="test",
            weight=1,
            threshold=1,
            permission="owner",
        )
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn("owner", op)
        self.assertIn(
            ["DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n", '1'],
            op["owner"]["key_auths"])
        self.assertEqual(op["owner"]["weight_threshold"], 1)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_disallow(self, node_param):
        if node_param == "non_appbase":
            acc = self.account
        elif node_param == "appbase":
            acc = self.account_appbase
        if sys.version > '3':
            _assertRaisesRegex = self.assertRaisesRegex
        else:
            _assertRaisesRegex = self.assertRaisesRegexp
        with _assertRaisesRegex(ValueError, ".*Changes nothing.*"):
            acc.disallow(
                "DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
                weight=1,
                threshold=1,
                permission="owner"
            )
        with _assertRaisesRegex(ValueError, ".*Changes nothing!.*"):
            acc.disallow(
                "DWB6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
                weight=1,
                threshold=1,
                permission="owner"
            )

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_update_memo_key(self, node_param):
        if node_param == "non_appbase":
            acc = self.account
        elif node_param == "appbase":
            acc = self.account_appbase
        acc.dpay.txbuffer.clear()
        tx = acc.update_memo_key("DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertEqual(
            op["memo_key"],
            "DWB55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_approvewitness(self, node_param):
        if node_param == "non_appbase":
            w = self.account
        elif node_param == "appbase":
            w = self.account_appbase
        w.dpay.txbuffer.clear()
        tx = w.approvewitness("test1")
        self.assertEqual(
            (tx["operations"][0][0]),
            "account_witness_vote"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "test1",
            op["witness"])

    def test_post(self):
        bts = self.bts
        bts.txbuffer.clear()
        tx = bts.post("title", "body", author="test", permlink=None, reply_identifier=None,
                      json_metadata=None, comment_options=None, community="test", tags=["a", "b", "c", "d", "e"],
                      beneficiaries=[{'account': 'test1', 'weight': 5000}, {'account': 'test2', 'weight': 5000}], self_vote=True)
        self.assertEqual(
            (tx["operations"][0][0]),
            "comment"
        )
        op = tx["operations"][0][1]
        self.assertEqual(op["body"], "body")
        self.assertEqual(op["title"], "title")
        self.assertEqual(op["permlink"], "title")
        self.assertEqual(op["parent_author"], "")
        self.assertEqual(op["parent_permlink"], "a")
        json_metadata = json.loads(op["json_metadata"])
        self.assertEqual(json_metadata["tags"], ["a", "b", "c", "d", "e"])
        self.assertEqual(json_metadata["app"], "dpaygo/%s" % (dpaygo_version))
        self.assertEqual(
            (tx["operations"][1][0]),
            "comment_options"
        )
        op = tx["operations"][1][1]
        self.assertEqual(len(op['extensions'][0][1]['beneficiaries']), 2)

    def test_comment_option(self):
        bts = self.bts
        bts.txbuffer.clear()
        tx = bts.comment_options({}, "@gtg/witness-gtg-log", account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "comment_options"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "gtg",
            op["author"])
        self.assertEqual('1000000.000 BBD', op["max_accepted_payout"])
        self.assertEqual(10000, op["percent_dpay_dollars"])
        self.assertEqual(True, op["allow_votes"])
        self.assertEqual(True, op["allow_curation_rewards"])
        self.assertEqual("witness-gtg-log", op["permlink"])

    def test_online(self):
        bts = self.bts
        self.assertFalse(bts.get_blockchain_version() == '0.0.0')

    def test_offline(self):
        bts = DPay(node=self.nodelist.get_nodes(appbase=False),
                    offline=True,
                    data_refresh_time_seconds=900,
                    keys={"active": wif, "owner": wif, "memo": wif})
        bts.refresh_data()
        self.assertTrue(bts.get_reserve_ratio(use_stored_data=False) is None)
        self.assertTrue(bts.get_reserve_ratio(use_stored_data=True) is None)
        self.assertTrue(bts.get_feed_history(use_stored_data=False) is None)
        self.assertTrue(bts.get_feed_history(use_stored_data=True) is None)
        self.assertTrue(bts.get_reward_funds(use_stored_data=False) is None)
        self.assertTrue(bts.get_reward_funds(use_stored_data=True) is None)
        self.assertTrue(bts.get_current_median_history(use_stored_data=False) is None)
        self.assertTrue(bts.get_current_median_history(use_stored_data=True) is None)
        self.assertTrue(bts.get_hardfork_properties(use_stored_data=False) is None)
        self.assertTrue(bts.get_hardfork_properties(use_stored_data=True) is None)
        self.assertTrue(bts.get_network(use_stored_data=False) is None)
        self.assertTrue(bts.get_network(use_stored_data=True) is None)
        self.assertTrue(bts.get_witness_schedule(use_stored_data=False) is None)
        self.assertTrue(bts.get_witness_schedule(use_stored_data=True) is None)
        self.assertTrue(bts.get_config(use_stored_data=False) is None)
        self.assertTrue(bts.get_config(use_stored_data=True) is None)
        self.assertEqual(bts.get_block_interval(), 3)
        self.assertEqual(bts.get_blockchain_version(), '0.0.0')

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_properties(self, node_param):
        if node_param == "non_appbase":
            bts = DPay(node=self.nodelist.get_nodes(appbase=False),
                        nobroadcast=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        elif node_param == "appbase":
            bts = DPay(node=self.nodelist.get_nodes(normal=False, appbase=True),
                        nobroadcast=True,
                        data_refresh_time_seconds=900,
                        keys={"active": wif, "owner": wif, "memo": wif},
                        num_retries=10)
        self.assertTrue(bts.get_reserve_ratio(use_stored_data=False) is not None)
        self.assertTrue(bts.get_feed_history(use_stored_data=False) is not None)
        self.assertTrue(bts.get_reward_funds(use_stored_data=False) is not None)
        self.assertTrue(bts.get_current_median_history(use_stored_data=False) is not None)
        self.assertTrue(bts.get_hardfork_properties(use_stored_data=False) is not None)
        self.assertTrue(bts.get_network(use_stored_data=False) is not None)
        self.assertTrue(bts.get_witness_schedule(use_stored_data=False) is not None)
        self.assertTrue(bts.get_config(use_stored_data=False) is not None)
        self.assertTrue(bts.get_block_interval() is not None)
        self.assertTrue(bts.get_blockchain_version() is not None)

    def test_sp_to_rshares(self):
        stm = self.bts
        rshares = stm.sp_to_rshares(stm.vests_to_sp(1e6))
        self.assertTrue(abs(rshares - 20000000000.0) < 2)

    def test_rshares_to_vests(self):
        stm = self.bts
        rshares = stm.sp_to_rshares(stm.vests_to_sp(1e6))
        rshares2 = stm.vests_to_rshares(1e6)
        self.assertTrue(abs(rshares - rshares2) < 2)

    def test_sp_to_bbd'(self):
        stm = self.bts
        sp = 500
        ret = stm.sp_to_bbd'(sp)
        self.assertTrue(ret is not None)

    def test_bbd'_to_rshares(self):
        stm = self.bts
        test_values = [1, 10, 100, 1e3, 1e4, 1e5, 1e6, 1e7]
        for v in test_values:
            try:
                bbd' = round(stm.rshares_to_bbd'(stm.bbd'_to_rshares(v)), 5)
            except ValueError:  # Reward pool smaller than 1e7 BBD (e.g. caused by a very low BEX price)
                continue
            self.assertEqual(bbd', v)

    def test_rshares_to_vote_pct(self):
        stm = self.bts
        sp = 1000
        voting_power = 9000
        for vote_pct in range(500, 10000, 500):
            rshares = stm.sp_to_rshares(sp, voting_power=voting_power, vote_pct=vote_pct)
            vote_pct_ret = stm.rshares_to_vote_pct(rshares, dpay_power=sp, voting_power=voting_power)
            self.assertEqual(vote_pct_ret, vote_pct)

    def test_sign(self):
        bts = self.bts
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            bts.sign()

    def test_broadcast(self):
        bts = self.bts
        bts.txbuffer.clear()
        tx = bts.comment_options({}, "@gtg/witness-gtg-log", account="test")
        # tx = bts.sign()
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            bts.broadcast(tx=tx)
