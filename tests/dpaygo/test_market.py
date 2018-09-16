from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import super
import unittest
from parameterized import parameterized
from pprint import pprint
from dpaygo import DPay
from dpaygo.market import Market
from dpaygo.price import Price
from dpaygo.asset import Asset
from dpaygo.amount import Amount
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
    def test_market(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m1 = Market(u'BEX', u'BBD', dpay_instance=bts)
        self.assertEqual(m1.get_string(), u'BBD:BEX')
        m2 = Market(dpay_instance=bts)
        self.assertEqual(m2.get_string(), u'BBD:BEX')
        m3 = Market(u'BEX:BBD', dpay_instance=bts)
        self.assertEqual(m3.get_string(), u'BEX:BBD')
        self.assertTrue(m1 == m2)

        base = Asset("BBD", dpay_instance=bts)
        quote = Asset("BEX", dpay_instance=bts)
        m = Market(base, quote, dpay_instance=bts)
        self.assertEqual(m.get_string(), u'BEX:BBD')

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_ticker(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        ticker = m.ticker()
        self.assertEqual(len(ticker), 6)
        self.assertEqual(ticker['dpay_volume']["symbol"], u'BEX')
        self.assertEqual(ticker['bbd_volume']["symbol"], u'BBD')

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_volume(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        volume = m.volume24h()
        self.assertEqual(volume['BEX']["symbol"], u'BEX')
        self.assertEqual(volume['BBD']["symbol"], u'BBD')

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_orderbook(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        orderbook = m.orderbook(limit=10)
        self.assertEqual(len(orderbook['asks_date']), 10)
        self.assertEqual(len(orderbook['asks']), 10)
        self.assertEqual(len(orderbook['bids_date']), 10)
        self.assertEqual(len(orderbook['bids']), 10)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_recenttrades(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        recenttrades = m.recent_trades(limit=10)
        recenttrades_raw = m.recent_trades(limit=10, raw_data=True)
        self.assertEqual(len(recenttrades), 10)
        self.assertEqual(len(recenttrades_raw), 10)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_trades(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        trades = m.trades(limit=10)
        trades_raw = m.trades(limit=10, raw_data=True)
        trades_history = m.trade_history(limit=10)
        self.assertEqual(len(trades), 10)
        self.assertTrue(len(trades_history) > 0)
        self.assertEqual(len(trades_raw), 10)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_market_history(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        buckets = m.market_history_buckets()
        history = m.market_history(buckets[2])
        self.assertTrue(len(history) > 0)

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_accountopenorders(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        openOrder = m.accountopenorders("test")
        self.assertTrue(isinstance(openOrder, list))

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_buy(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        m = Market(u'BEX:BBD', dpay_instance=bts)
        bts.txbuffer.clear()
        tx = m.buy(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.100 BEX', dpay_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"BBD:BEX", dpay_instance=bts)
        tx = m.buy(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.100 BEX', dpay_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"BBD:BEX", dpay_instance=bts)
        a = Amount(0.1, "BEX", dpay_instance=bts)
        tx = m.buy(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(a), op["min_to_receive"])
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["amount_to_sell"])

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_sell(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        bts.txbuffer.clear()
        m = Market(u'BEX:BBD', dpay_instance=bts)
        tx = m.sell(5, 0.1, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_create"
        )
        op = tx["operations"][0][1]
        self.assertIn("test", op["owner"])
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 BEX', dpay_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"BBD:BEX")
        tx = m.sell(p, 0.1, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 BEX', dpay_instance=bts)), op["amount_to_sell"])

        p = Price(5, u"BBD:BEX", dpay_instance=bts)
        a = Amount(0.1, "BEX", dpay_instance=bts)
        tx = m.sell(p, a, account="test")
        op = tx["operations"][0][1]
        self.assertEqual(str(Amount('0.500 BBD', dpay_instance=bts)), op["min_to_receive"])
        self.assertEqual(str(Amount('0.100 BEX', dpay_instance=bts)), op["amount_to_sell"])

    @parameterized.expand([
        ("non_appbase"),
        ("appbase"),
    ])
    def test_cancel(self, node_param):
        if node_param == "non_appbase":
            bts = self.bts
        else:
            bts = self.appbase
        bts.txbuffer.clear()
        m = Market(u'BEX:BBD', dpay_instance=bts)
        tx = m.cancel(5, account="test")
        self.assertEqual(
            (tx["operations"][0][0]),
            "limit_order_cancel"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "test",
            op["owner"])

    def test_dpay_usb_impied(self):
        bts = self.bts
        m = Market(u'BEX:BBD', dpay_instance=bts)
        dpay_usd = m.dpay_usd_implied()
        self.assertGreater(dpay_usd, 0)
