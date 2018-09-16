from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from dpaygo import DPay
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.transactionbuilder import TransactionBuilder
from dpaygobase.signedtransactions import Signed_Transaction
from dpaygobase.operations import Transfer
from dpaygo.account import Account
from dpaygo.block import Block
from dpaygographenebase.base58 import Base58
from dpaygo.amount import Amount
from dpaygo.exceptions import (
    InsufficientAuthorityError,
    MissingKeyError,
    InvalidWifError,
    WalletLocked
)
from dpaygoapi import exceptions
from dpaygo.wallet import Wallet
from dpaygo.utils import formatTimeFromNow
from dpaygo.nodelist import NodeList
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        cls.stm = DPay(
            node=nodelist.get_nodes(appbase=False),
            keys={"active": wif, "owner": wif, "memo": wif},
            nobroadcast=True,
            num_retries=10
        )
        cls.appbase = DPay(
            node=nodelist.get_nodes(normal=False, appbase=True),
            nobroadcast=True,
            keys={"active": wif, "owner": wif, "memo": wif},
            num_retries=10
        )
        set_shared_dpay_instance(cls.stm)
        cls.stm.set_default_account("test")

    def test_emptyTransaction(self):
        stm = self.stm
        tx = TransactionBuilder(dpay_instance=stm)
        self.assertTrue(tx.is_empty())
        self.assertTrue(tx["ref_block_num"] is not None)

    def test_verify_transaction(self):
        stm = self.stm
        block = Block(22005665, dpay_instance=stm)
        trx = block.transactions[28]
        signed_tx = Signed_Transaction(trx)
        key = signed_tx.verify(chain=stm.chain_params, recover_parameter=False)
        public_key = format(Base58(key[0]), stm.prefix)
        self.assertEqual(public_key, "DWB4tzr1wjmuov9ftXR6QNv7qDWsbShMBPQpuwatZsfSc5pKjRDfq")
