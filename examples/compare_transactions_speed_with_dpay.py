from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import bytes
from builtins import chr
from builtins import range
from builtins import super
import random
from pprint import pprint
from binascii import hexlify
from collections import OrderedDict

from dpaygobase import (
    transactions,
    memo,
    operations,
    objects
)
from dpaygobase.objects import Operation
from dpaygobase.signedtransactions import Signed_Transaction
from dpaygographenebase.account import PrivateKey
from dpaygographenebase import account
from dpaygobase.operationids import getOperationNameForId
from dpaygographenebase.py23 import py23_bytes, bytes_types
from dpaygo.amount import Amount
from dpaygo.asset import Asset
from dpaygo.dpay import DPay
import time

from dpay import DPay as dpayDPay
from dpaybase.account import PrivateKey as dpayPrivateKey
from dpaybase.transactions import SignedTransaction as dpaySignedTransaction
from dpaybase import operations as dpayOperations
from timeit import default_timer as timer


class DPayGoTest(object):

    def setup(self):
        self.prefix = u"BEX"
        self.default_prefix = u"DWB"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"
        self.stm = DPay(offline=True)

    def doit(self, printWire=False, ops=None):
        ops = [Operation(ops)]
        tx = Signed_Transaction(ref_block_num=self.ref_block_num,
                                ref_block_prefix=self.ref_block_prefix,
                                expiration=self.expiration,
                                operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([PrivateKey(self.wif, prefix=u"DWB").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


class DPayTest(object):

    def setup(self):
        self.prefix = u"BEX"
        self.default_prefix = u"DWB"
        self.wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
        self.ref_block_num = 34294
        self.ref_block_prefix = 3707022213
        self.expiration = "2016-04-06T08:29:27"

    def doit(self, printWire=False, ops=None):
        ops = [dpayOperations.Operation(ops)]
        tx = dpaySignedTransaction(ref_block_num=self.ref_block_num,
                                    ref_block_prefix=self.ref_block_prefix,
                                    expiration=self.expiration,
                                    operations=ops)
        start = timer()
        tx = tx.sign([self.wif], chain=self.prefix)
        end1 = timer()
        tx.verify([dpayPrivateKey(self.wif, prefix=u"DWB").pubkey], self.prefix)
        end2 = timer()
        return end2 - end1, end1 - start


if __name__ == "__main__":
    dpay_test = DPayTest()
    dpaygo_test = DPayGoTest()
    dpay_test.setup()
    dpaygo_test.setup()
    dpay_times = []
    dpaygo_times = []
    loops = 50
    for i in range(0, loops):
        print(i)
        opDPay = dpayOperations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": "111.110 BEX",
            "memo": "Fooo"
        })
        opDPayGo = operations.Transfer(**{
            "from": "foo",
            "to": "baar",
            "amount": Amount("111.110 BEX", dpay_instance=DPay(offline=True)),
            "memo": "Fooo"
        })

        t_s, t_v = dpay_test.doit(ops=opDPay)
        dpay_times.append([t_s, t_v])

        t_s, t_v = dpaygo_test.doit(ops=opDPayGo)
        dpaygo_times.append([t_s, t_v])

    dpay_dt = [0, 0]
    dpaygo_dt = [0, 0]
    for i in range(0, loops):
        dpay_dt[0] += dpay_times[i][0]
        dpay_dt[1] += dpay_times[i][1]
        dpaygo_dt[0] += dpaygo_times[i][0]
        dpaygo_dt[1] += dpaygo_times[i][1]
    print("dpaycli vs dpaygo:\n")
    print("dpaycli: sign: %.2f s, verification %.2f s" % (dpay_dt[0] / loops, dpay_dt[1] / loops))
    print("dpaygo:  sign: %.2f s, verification %.2f s" % (dpaygo_dt[0] / loops, dpaygo_dt[1] / loops))
    print("------------------------------------")
    print("dpaygo is %.2f %% (sign) and %.2f %% (verify) faster than dpay" %
          (dpay_dt[0] / dpaygo_dt[0] * 100, dpay_dt[1] / dpaygo_dt[1] * 100))
