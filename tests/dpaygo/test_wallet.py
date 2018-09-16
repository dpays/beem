from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
import mock
from pprint import pprint
from dpaygo import DPay, exceptions
from dpaygo.account import Account
from dpaygo.amount import Amount
from dpaygo.asset import Asset
from dpaygo.wallet import Wallet
from dpaygo.instance import set_shared_dpay_instance, shared_dpay_instance
from dpaygo.nodelist import NodeList

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        stm = shared_dpay_instance()
        stm.config.refreshBackup()
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))

        cls.stm = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            num_retries=10
            # Overwrite wallet to use this list of wifs only
        )
        cls.appbase = DPay(
            node=nodelist.get_nodes(normal=False, appbase=True),
            nobroadcast=True,
            bundle=True,
            num_retries=10
        )
        cls.stm.set_default_account("test")
        set_shared_dpay_instance(cls.stm)
        # self.stm.newWallet("TestingOneTwoThree")

        cls.wallet = Wallet(dpay_instance=cls.stm)
        cls.wallet.wipe(True)
        cls.wallet.newWallet(pwd="TestingOneTwoThree")
        cls.wallet.unlock(pwd="TestingOneTwoThree")
        cls.wallet.addPrivateKey(wif)

    @classmethod
    def tearDownClass(cls):
        stm = shared_dpay_instance()
        stm.config.recover_with_latest_backup()

    def test_wallet_lock(self):
        stm = self.stm
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.assertTrue(self.wallet.unlocked())
        self.assertFalse(self.wallet.locked())
        self.wallet.lock()
        self.assertTrue(self.wallet.locked())

    def test_change_masterpassword(self):
        stm = self.stm
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.assertTrue(self.wallet.unlocked())
        self.wallet.changePassphrase("newPass")
        self.wallet.lock()
        self.assertTrue(self.wallet.locked())
        self.wallet.unlock(pwd="newPass")
        self.assertTrue(self.wallet.unlocked())
        self.wallet.changePassphrase("TestingOneTwoThree")
        self.wallet.lock()

    def test_Keys(self):
        stm = self.stm
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        keys = self.wallet.getPublicKeys()
        self.assertTrue(len(keys) > 0)
        pub = self.wallet.getPublicKeys()[0]
        private = self.wallet.getPrivateKeyForPublicKey(pub)
        self.assertEqual(private, wif)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_account_by_pub(self, node_param):
        if node_param == "non_appbase":
            stm = self.stm
        else:
            stm = self.appbase
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        acc = Account("gtg")
        pub = acc["owner"]["key_auths"][0][0]
        acc_by_pub = self.wallet.getAccount(pub)
        self.assertEqual("gtg", acc_by_pub["name"])
        gen = self.wallet.getAccountsFromPublicKey(pub)
        acc_by_pub_list = []
        for a in gen:
            acc_by_pub_list.append(a)
        self.assertEqual("gtg", acc_by_pub_list[0])
        gen = self.wallet.getAllAccounts(pub)
        acc_by_pub_list = []
        for a in gen:
            acc_by_pub_list.append(a)
        self.assertEqual("gtg", acc_by_pub_list[0]["name"])
        self.assertEqual(pub, acc_by_pub_list[0]["pubkey"])

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_pub_lookup(self, node_param):
        if node_param == "non_appbase":
            stm = self.stm
        else:
            stm = self.appbase
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getOwnerKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getMemoKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getActiveKeyForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getPostingKeyForAccount("test")

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_pub_lookup_keys(self, node_param):
        if node_param == "non_appbase":
            stm = self.stm
        else:
            stm = self.appbase
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getOwnerKeysForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getActiveKeysForAccount("test")
        with self.assertRaises(
            exceptions.MissingKeyError
        ):
            self.wallet.getPostingKeysForAccount("test")

    def test_encrypt(self):
        stm = self.stm
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.wallet.masterpassword = "TestingOneTwoThree"
        self.assertEqual([self.wallet.encrypt_wif("5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),
                          self.wallet.encrypt_wif("5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR")],
                         ["6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi",
                          "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg"])
        self.wallet.masterpassword = "Satoshi"
        self.assertEqual([self.wallet.encrypt_wif("5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5")],
                         ["6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq"])
        self.wallet.masterpassword = "TestingOneTwoThree"

    def test_deencrypt(self):
        stm = self.stm
        self.wallet.dpay = stm
        self.wallet.unlock(pwd="TestingOneTwoThree")
        self.wallet.masterpassword = "TestingOneTwoThree"
        self.assertEqual([self.wallet.decrypt_wif("6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi"),
                          self.wallet.decrypt_wif("6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg")],
                         ["5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",
                          "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR"])
        self.wallet.masterpassword = "Satoshi"
        self.assertEqual([self.wallet.decrypt_wif("6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq")],
                         ["5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"])
        self.wallet.masterpassword = "TestingOneTwoThree"
