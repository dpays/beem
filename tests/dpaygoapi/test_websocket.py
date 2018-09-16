from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import range
from builtins import super
import mock
import string
import unittest
import random
import itertools
from pprint import pprint
from dpaygo import DPay
from dpaygoapi.websocket import DPayWebsocket
from dpaygo.instance import set_shared_dpay_instance
from dpaygo.nodelist import NodeList
# Py3 compatibility
import sys

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "DWB"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nodelist = NodeList()
        nodelist.update_nodes(dpay_instance=DPay(node=nodelist.get_nodes(normal=True, appbase=True), num_retries=10))
        stm = DPay(node=nodelist.get_nodes(appbase=False))

        self.ws = DPayWebsocket(
            urls=stm.rpc.nodes,
            num_retries=10
        )

    def test_connect(self):
        ws = self.ws
        self.assertTrue(len(next(ws.nodes)) > 0)
