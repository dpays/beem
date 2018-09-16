# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import unittest
import json
from dpaygographenebase import types
from dpaygo.amount import Amount
from dpaygo import DPay


class Testcases(unittest.TestCase):
    def test_JsonObj(self):
        j = {"a": 2, "b": "abcde", "c": ["a", "b"]}
        j2 = types.JsonObj(json.dumps(j))
        self.assertEqual(j, j2)

        stm = DPay(
            offline=True
        )
        a = Amount("1 BBD", dpay_instance=stm)
        j = a.json()
        j2 = types.JsonObj(json.dumps(j))
        self.assertEqual(j, j2)
