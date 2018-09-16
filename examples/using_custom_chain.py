from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys
from datetime import datetime, timedelta
import time
import io
import logging

from dpaygo.blockchain import Blockchain
from dpaygo.block import Block
from dpaygo.account import Account
from dpaygo.amount import Amount
from dpaygographenebase.account import PasswordKey, PrivateKey, PublicKey
from dpaygo.dpay import DPay
from dpaygo.utils import parse_time, formatTimedelta
from dpaygoapi.exceptions import NumRetriesReached
from dpaygo.nodelist import NodeList
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    stm = DPay(node=["https://testnet.dpays.io"],
                custom_chains={"TESTNETHF20":
                               {'chain_assets':
                                [
                                    {"asset": "@@000000013", "symbol": "BBD", "precision": 3, "id": 0},
                                    {"asset": "@@000000021", "symbol": "BET", "precision": 3, "id": 1},
                                    {"asset": "@@000000037", "symbol": "VESTS", "precision": 6, "id": 2}
                                ],
                                'chain_id': '46d82ab7d8db682eb1959aed0ada039a6d49afa1602491f93dde9cac3e8e6c32',
                                'min_version': '0.20.0',
                                'prefix': 'DWT'}})
    print(stm.get_blockchain_version())
    print(stm.get_config()["DPAY_CHAIN_ID"])
