from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from dpaygo import DPay
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.amount import Amount
from dpaygo.price import Price, Order, FilledOrder
from dpaygo.asset import Asset
import unittest
from dpaygo.nodelist import NodeList


class Testcases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        dpay = DPay(
            node=nodelist.get_nodes(appbase=False),
            nobroadcast=True,
            num_retries=10
        )
        set_shared_dpay_instance(dpay)

    def test_init(self):
        # self.assertEqual(1, 1)

        Price("0.315 BEX/BBD")
        Price(1.0, "BEX/BBD")
        Price(0.315, base="BEX", quote="BBD")
        Price(0.315, base=Asset("BEX"), quote=Asset("BBD"))
        Price({
            "base": {"amount": 1, "asset_id": "BBD"},
            "quote": {"amount": 10, "asset_id": "BEX"}})
        Price("", quote="10 BBD", base="1 BEX")
        Price("10 BBD", "1 BEX")
        Price(Amount("10 BBD"), Amount("1 BEX"))

    def test_multiplication(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "VESTS/BEX")
        p3 = p1 * p2
        p4 = p3.as_base("BBD")
        p4_2 = p3.as_quote("VESTS")

        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "BBD")
        # 10 BEX/BBD * 0.2 VESTS/BEX = 50 VESTS/BBD = 0.02 BBD/VESTS
        self.assertEqual(float(p4), 0.02)
        self.assertEqual(p4_2["quote"]["symbol"], "VESTS")
        self.assertEqual(p4_2["base"]["symbol"], "BBD")
        self.assertEqual(float(p4_2), 0.02)
        p3 = p1 * 5
        self.assertEqual(float(p3), 50)

        # Inline multiplication
        p5 = Price(10.0, "BEX/BBD")
        p5 *= p2
        p4 = p5.as_base("BBD")
        self.assertEqual(p4["quote"]["symbol"], "VESTS")
        self.assertEqual(p4["base"]["symbol"], "BBD")
        # 10 BEX/BBD * 0.2 VESTS/BEX = 2 VESTS/BBD = 0.02 BBD/VESTS
        self.assertEqual(float(p4), 0.02)
        p6 = Price(10.0, "BEX/BBD")
        p6 *= 5
        self.assertEqual(float(p6), 50)

    def test_div(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "BEX/VESTS")

        # 10 BEX/BBD / 5 BEX/VESTS = 2 VESTS/BBD
        p3 = p1 / p2
        p4 = p3.as_base("VESTS")
        self.assertEqual(p4["base"]["symbol"], "VESTS")
        self.assertEqual(p4["quote"]["symbol"], "BBD")
        # 10 BEX/BBD * 0.2 VESTS/BEX = 2 VESTS/BBD = 0.5 BBD/VESTS
        self.assertEqual(float(p4), 2)

    def test_div2(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "BEX/BBD")

        # 10 BEX/BBD / 5 BEX/VESTS = 2 VESTS/BBD
        p3 = p1 / p2
        self.assertTrue(isinstance(p3, (float, int)))
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / 5
        self.assertEqual(float(p3), 2.0)
        p3 = p1 / Amount("1 BBD")
        self.assertEqual(float(p3), 0.1)
        p3 = p1
        p3 /= p2
        self.assertEqual(float(p3), 2.0)
        p3 = p1
        p3 /= 5
        self.assertEqual(float(p3), 2.0)

    def test_ltge(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "BEX/BBD")

        self.assertTrue(p1 > p2)
        self.assertTrue(p2 < p1)
        self.assertTrue(p1 > 5)
        self.assertTrue(p2 < 10)

    def test_leeq(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "BEX/BBD")

        self.assertTrue(p1 >= p2)
        self.assertTrue(p2 <= p1)
        self.assertTrue(p1 >= 5)
        self.assertTrue(p2 <= 10)

    def test_ne(self):
        p1 = Price(10.0, "BEX/BBD")
        p2 = Price(5.0, "BEX/BBD")

        self.assertTrue(p1 != p2)
        self.assertTrue(p1 == p1)
        self.assertTrue(p1 != 5)
        self.assertTrue(p1 == 10)

    def test_order(self):
        order = Order(Amount("2 BBD"), Amount("1 BEX"))
        self.assertTrue(repr(order) is not None)

    def test_filled_order(self):
        order = {"date": "1900-01-01T00:00:00", "current_pays": "2 BBD", "open_pays": "1 BEX"}
        filledOrder = FilledOrder(order)
        self.assertTrue(repr(filledOrder) is not None)
        self.assertEqual(filledOrder.json()["current_pays"], "2.000 BBD")
