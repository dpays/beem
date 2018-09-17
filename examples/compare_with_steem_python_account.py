from __future__ import print_function
import sys
from datetime import timedelta
import time
import io
from dpaygo import DPay
from dpaygo.account import Account
from dpaygo.amount import Amount
from dpaygo.utils import parse_time
from dpay.account import Account as dpayAccount
from dpay.post import Post as dpayPost
from dpay import DPay as dpayDPay
import logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    stm = DPay("wss://dpayd.dpays.io")
    dpaygo_acc = Account("jared", dpay_instance=stm)
    stm2 = dpayDPay(nodes=["wss://dpayd.dpays.io"])
    dpay_acc = dpayAccount("jared", dpayd_instance=stm2)

    # profile
    print("dpaygo_acc.profile  {}".format(dpaygo_acc.profile))
    print("dpay_acc.profile {}".format(dpay_acc.profile))
    # sp
    print("dpaygo_acc.sp  {}".format(dpaygo_acc.sp))
    print("dpay_acc.sp {}".format(dpay_acc.sp))
    # rep
    print("dpaygo_acc.rep  {}".format(dpaygo_acc.rep))
    print("dpay_acc.rep {}".format(dpay_acc.rep))
    # balances
    print("dpaygo_acc.balances  {}".format(dpaygo_acc.balances))
    print("dpay_acc.balances {}".format(dpay_acc.balances))
    # get_balances()
    print("dpaygo_acc.get_balances()  {}".format(dpaygo_acc.get_balances()))
    print("dpay_acc.get_balances() {}".format(dpay_acc.get_balances()))
    # reputation()
    print("dpaygo_acc.get_reputation()  {}".format(dpaygo_acc.get_reputation()))
    print("dpay_acc.reputation() {}".format(dpay_acc.reputation()))
    # voting_power()
    print("dpaygo_acc.get_voting_power()  {}".format(dpaygo_acc.get_voting_power()))
    print("dpay_acc.voting_power() {}".format(dpay_acc.voting_power()))
    # get_followers()
    print("dpaygo_acc.get_followers()  {}".format(dpaygo_acc.get_followers()))
    print("dpay_acc.get_followers() {}".format(dpay_acc.get_followers()))
    # get_following()
    print("dpaygo_acc.get_following()  {}".format(dpaygo_acc.get_following()))
    print("dpay_acc.get_following() {}".format(dpay_acc.get_following()))
    # has_voted()
    print("dpaygo_acc.has_voted()  {}".format(dpaygo_acc.has_voted("@jared/api-methods-list-for-appbase")))
    print("dpay_acc.has_voted() {}".format(dpay_acc.has_voted(dpayPost("@jared/api-methods-list-for-appbase"))))
    # curation_stats()
    print("dpaygo_acc.curation_stats()  {}".format(dpaygo_acc.curation_stats()))
    print("dpay_acc.curation_stats() {}".format(dpay_acc.curation_stats()))
    # virtual_op_count
    print("dpaygo_acc.virtual_op_count()  {}".format(dpaygo_acc.virtual_op_count()))
    print("dpay_acc.virtual_op_count() {}".format(dpay_acc.virtual_op_count()))
    # get_account_votes
    print("dpaygo_acc.get_account_votes()  {}".format(dpaygo_acc.get_account_votes()))
    print("dpay_acc.get_account_votes() {}".format(dpay_acc.get_account_votes()))
    # get_withdraw_routes
    print("dpaygo_acc.get_withdraw_routes()  {}".format(dpaygo_acc.get_withdraw_routes()))
    print("dpay_acc.get_withdraw_routes() {}".format(dpay_acc.get_withdraw_routes()))
    # get_conversion_requests
    print("dpaygo_acc.get_conversion_requests()  {}".format(dpaygo_acc.get_conversion_requests()))
    print("dpay_acc.get_conversion_requests() {}".format(dpay_acc.get_conversion_requests()))
    # export
    # history
    dpaygo_hist = []
    for h in dpaygo_acc.history(only_ops=["transfer"]):
        dpaygo_hist.append(h)
        if len(dpaygo_hist) >= 10:
            break
    dpay_hist = []
    for h in dpay_acc.history(filter_by="transfer", start=0):
        dpay_hist.append(h)
        if len(dpay_hist) >= 10:
            break
    print("dpaygo_acc.history()  {}".format(dpaygo_hist))
    print("dpay_acc.history() {}".format(dpay_hist))
    # history_reverse
    dpaygo_hist = []
    for h in dpaygo_acc.history_reverse(only_ops=["transfer"]):
        dpaygo_hist.append(h)
        if len(dpaygo_hist) >= 10:
            break
    dpay_hist = []
    for h in dpay_acc.history_reverse(filter_by="transfer"):
        dpay_hist.append(h)
        if len(dpay_hist) >= 10:
            break
    print("dpaygo_acc.history_reverse()  {}".format(dpaygo_hist))
    print("dpay_acc.history_reverse() {}".format(dpay_hist))
