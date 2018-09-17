#!/usr/bin/python
import sys
import datetime as dt
from dpaygo.amount import Amount
from dpaygo.utils import parse_time, formatTimeString, addTzInfo
from dpaygo.instance import set_shared_dpay_instance
from dpaygo import DPay
from dpaygo.snapshot import AccountSnapshot
import matplotlib as mpl
# mpl.use('Agg')
# mpl.use('TkAgg')
import matplotlib.pyplot as plt


if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("ERROR: command line parameter mismatch!")
        # print("usage: %s [account]" % (sys.argv[0]))
        account = "holger80"
    else:
        account = sys.argv[1]
    acc_snapshot = AccountSnapshot(account)
    acc_snapshot.get_account_history()
    acc_snapshot.build()
    # acc_snapshot.build(only_ops=["producer_reward"])
    # acc_snapshot.build(only_ops=["curation_reward"])
    # acc_snapshot.build(only_ops=["author_reward"])
    acc_snapshot.build_bp_arrays()
    timestamps = acc_snapshot.timestamps
    own_sp = acc_snapshot.own_sp
    eff_sp = acc_snapshot.eff_sp

    plt.figure(figsize=(12, 6))
    opts = {'linestyle': '-', 'marker': '.'}
    plt.plot_date(timestamps[1:], own_sp[1:], label="Own BP", **opts)
    plt.plot_date(timestamps[1:], eff_sp[1:], label="Effective BP", **opts)
    plt.grid()
    plt.legend()
    plt.title("BP over time - @%s" % (account))
    plt.xlabel("Date")
    plt.ylabel("BEX Power (BP)")
    # plt.show()
    plt.savefig("bp_over_time-%s.png" % (account))

    print("last effective BP: %.1f BP" % (eff_sp[-1]))
    print("last own BP: %.1f BP" % (own_sp[-1]))
