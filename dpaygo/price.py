# This Python file uses the following encoding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import str
from future.utils import python_2_unicode_compatible
from dpaygographenebase.py23 import bytes_types, integer_types, string_types, text_type
from fractions import Fraction
from dpaygo.instance import shared_dpay_instance
from .exceptions import InvalidAssetException
from .account import Account
from .amount import Amount
from .asset import Asset
from .utils import formatTimeString
from .utils import parse_time, assets_from_string


@python_2_unicode_compatible
class Price(dict):
    """ This class deals with all sorts of prices of any pair of assets to
        simplify dealing with the tuple::

            (quote, base)

        each being an instance of :class:`dpaygo.amount.Amount`. The
        amount themselves define the price.

        .. note::

            The price (floating) is derived as ``base/quote``

        :param list args: Allows to deal with different representations of a price
        :param dpaygo.asset.Asset base: Base asset
        :param dpaygo.asset.Asset quote: Quote asset
        :param dpaygo.dpay.DPay dpay_instance: DPay instance
        :returns: All data required to represent a price
        :rtype: dict

        Way to obtain a proper instance:

            * ``args`` is a str with a price and two assets
            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of :class:`dpaygo.asset.Asset`
            * ``args`` can be a floating number and ``base`` and ``quote`` being instances of ``str``
            * ``args`` can be dict with keys ``price``, ``base``, and ``quote`` (*graphene balances*)
            * ``args`` can be dict with keys ``base`` and ``quote``
            * ``args`` can be dict with key ``receives`` (filled orders)
            * ``args`` being a list of ``[quote, base]`` both being instances of :class:`dpaygo.amount.Amount`
            * ``args`` being a list of ``[quote, base]`` both being instances of ``str`` (``amount symbol``)
            * ``base`` and ``quote`` being instances of :class:`dpaygo.asset.Amount`

        This allows instanciations like:

        * ``Price("0.315 BBD/BEX")``
        * ``Price(0.315, base="BBD", quote="BEX")``
        * ``Price(0.315, base=Asset("BBD"), quote=Asset("BEX"))``
        * ``Price({"base": {"amount": 1, "asset_id": "BBD"}, "quote": {"amount": 10, "asset_id": "BBD"}})``
        * ``Price(quote="10 BEX", base="1 BBD")``
        * ``Price("10 BEX", "1 BBD")``
        * ``Price(Amount("10 BEX"), Amount("1 BBD"))``
        * ``Price(1.0, "BBD/BEX")``

        Instances of this class can be used in regular mathematical expressions
        (``+-*/%``) such as:

        .. code-block:: python

            >>> from dpaygo.price import Price
            >>> Price("0.3314 BBD/BEX") * 2
            0.662804 BBD/BEX
            >>> Price(0.3314, "BBD", "BEX")
            0.331402 BBD/BEX

    """
    def __init__(
        self,
        price=None,
        base=None,
        quote=None,
        base_asset=None,  # to identify sell/buy
        dpay_instance=None
    ):

        self.dpay = dpay_instance or shared_dpay_instance()
        if price is "":
            price = None
        if (price is not None and isinstance(price, string_types) and not base and not quote):
            import re
            price, assets = price.split(" ")
            base_symbol, quote_symbol = assets_from_string(assets)
            base = Asset(base_symbol, dpay_instance=self.dpay)
            quote = Asset(quote_symbol, dpay_instance=self.dpay)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, dpay_instance=self.dpay)
            self["base"] = Amount(amount=frac.numerator, asset=base, dpay_instance=self.dpay)

        elif (price is not None and isinstance(price, dict) and
                "base" in price and
                "quote" in price):
            if "price" in price:
                raise AssertionError("You cannot provide a 'price' this way")
            # Regular 'price' objects according to dpay-core
            # base_id = price["base"]["asset_id"]
            # if price["base"]["asset_id"] == base_id:
            self["base"] = Amount(price["base"], dpay_instance=self.dpay)
            self["quote"] = Amount(price["quote"], dpay_instance=self.dpay)
            # else:
            #    self["quote"] = Amount(price["base"], dpay_instance=self.dpay)
            #    self["base"] = Amount(price["quote"], dpay_instance=self.dpay)

        elif (price is not None and isinstance(base, Asset) and isinstance(quote, Asset)):
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, dpay_instance=self.dpay)
            self["base"] = Amount(amount=frac.numerator, asset=base, dpay_instance=self.dpay)

        elif (price is not None and isinstance(base, string_types) and isinstance(quote, string_types)):
            base = Asset(base, dpay_instance=self.dpay)
            quote = Asset(quote, dpay_instance=self.dpay)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, dpay_instance=self.dpay)
            self["base"] = Amount(amount=frac.numerator, asset=base, dpay_instance=self.dpay)

        elif (price is None and isinstance(base, string_types) and isinstance(quote, string_types)):
            self["quote"] = Amount(quote, dpay_instance=self.dpay)
            self["base"] = Amount(base, dpay_instance=self.dpay)
        elif (price is not None and isinstance(price, string_types) and isinstance(base, string_types)):
            self["quote"] = Amount(price, dpay_instance=self.dpay)
            self["base"] = Amount(base, dpay_instance=self.dpay)
        # len(args) > 1

        elif isinstance(price, Amount) and isinstance(base, Amount):
            self["quote"], self["base"] = price, base

        # len(args) == 0
        elif (price is None and isinstance(base, Amount) and isinstance(quote, Amount)):
            self["quote"] = quote
            self["base"] = base

        elif ((isinstance(price, float) or isinstance(price, integer_types)) and
                isinstance(base, string_types)):
            import re
            base_symbol, quote_symbol = assets_from_string(base)
            base = Asset(base_symbol, dpay_instance=self.dpay)
            quote = Asset(quote_symbol, dpay_instance=self.dpay)
            frac = Fraction(float(price)).limit_denominator(10 ** base["precision"])
            self["quote"] = Amount(amount=frac.denominator, asset=quote, dpay_instance=self.dpay)
            self["base"] = Amount(amount=frac.numerator, asset=base, dpay_instance=self.dpay)

        else:
            raise ValueError("Couldn't parse 'Price'.")

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        if ("quote" in self and
                "base" in self and
                self["base"] and self["quote"]):  # don't derive price for deleted Orders
            dict.__setitem__(self, "price", self._safedivide(
                self["base"]["amount"],
                self["quote"]["amount"]))

    def copy(self):
        return Price(
            None,
            base=self["base"].copy(),
            quote=self["quote"].copy(),
            dpay_instance=self.dpay)

    def _safedivide(self, a, b):
        if b != 0.0:
            return a / b
        else:
            return float('Inf')

    def symbols(self):
        return self["base"]["symbol"], self["quote"]["symbol"]

    def as_base(self, base):
        """ Returns the price instance so that the base asset is ``base``.

            Note: This makes a copy of the object!

            .. code-block:: python

                >>> from dpaygo.price import Price
                >>> Price("0.3314 BBD/BEX").as_base("BEX")
                3.017483 BEX/BBD

        """
        if base == self["base"]["symbol"]:
            return self.copy()
        elif base == self["quote"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def as_quote(self, quote):
        """ Returns the price instance so that the quote asset is ``quote``.

            Note: This makes a copy of the object!

            .. code-block:: python

                >>> from dpaygo.price import Price
                >>> Price("0.3314 BBD/BEX").as_quote("BBD")
                3.017483 BEX/BBD

        """
        if quote == self["quote"]["symbol"]:
            return self.copy()
        elif quote == self["base"]["symbol"]:
            return self.copy().invert()
        else:
            raise InvalidAssetException

    def invert(self):
        """ Invert the price (e.g. go from ``BBD/BEX`` into ``BEX/BBD``)

            .. code-block:: python

                >>> from dpaygo.price import Price
                >>> Price("0.3314 BBD/BEX").invert()
                3.017483 BEX/BBD

        """
        tmp = self["quote"]
        self["quote"] = self["base"]
        self["base"] = tmp
        return self

    def json(self):
        return {
            "base": self["base"].json(),
            "quote": self["quote"].json()
        }

    def __repr__(self):
        return "{price:.{precision}f} {base}/{quote}".format(
            price=self["price"],
            base=self["base"]["symbol"],
            quote=self["quote"]["symbol"],
            precision=(
                self["base"]["asset"]["precision"] +
                self["quote"]["asset"]["precision"]
            )
        )

    def __float__(self):
        return self["price"]

    def _check_other(self, other):
        if not other["base"]["symbol"] == self["base"]["symbol"]:
            raise AssertionError()
        if not other["quote"]["symbol"] == self["quote"]["symbol"]:
            raise AssertionError()

    def __mul__(self, other):
        a = self.copy()
        if isinstance(other, Price):
            # Rotate/invert other
            if (
                self["quote"]["symbol"] not in other.symbols() and
                self["base"]["symbol"] not in other.symbols()
            ):
                raise InvalidAssetException

            # base/quote = a/b
            # a/b * b/c = a/c
            a = self.copy()
            if self["quote"]["symbol"] == other["base"]["symbol"]:
                a["base"] = Amount(
                    float(self["base"]) * float(other["base"]), self["base"]["symbol"],
                    dpay_instance=self.dpay
                )
                a["quote"] = Amount(
                    float(self["quote"]) * float(other["quote"]), other["quote"]["symbol"],
                    dpay_instance=self.dpay
                )
            # a/b * c/a =  c/b
            elif self["base"]["symbol"] == other["quote"]["symbol"]:
                a["base"] = Amount(
                    float(self["base"]) * float(other["base"]), other["base"]["symbol"],
                    dpay_instance=self.dpay
                )
                a["quote"] = Amount(
                    float(self["quote"]) * float(other["quote"]), self["quote"]["symbol"],
                    dpay_instance=self.dpay
                )
            else:
                raise ValueError("Wrong rotation of prices")
        elif isinstance(other, Amount):
            if not other["asset"] == self["quote"]["asset"]:
                raise AssertionError()
            a = other.copy() * self["price"]
            a["asset"] = self["base"]["asset"].copy()
            a["symbol"] = self["base"]["asset"]["symbol"]
        else:
            a["base"] *= other
        return a

    def __imul__(self, other):
        if isinstance(other, Price):
            tmp = self * other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] *= other
        return self

    def __div__(self, other):
        a = self.copy()
        if isinstance(other, Price):
            # Rotate/invert other
            if sorted(self.symbols()) == sorted(other.symbols()):
                return float(self.as_base(self["base"]["symbol"])) / float(other.as_base(self["base"]["symbol"]))
            elif self["quote"]["symbol"] in other.symbols():
                other = other.as_base(self["quote"]["symbol"])
            elif self["base"]["symbol"] in other.symbols():
                other = other.as_base(self["base"]["symbol"])
            else:
                raise InvalidAssetException
            a["base"] = Amount(
                float(self["base"].amount / other["base"].amount), other["quote"]["symbol"],
                dpay_instance=self.dpay
            )
            a["quote"] = Amount(
                float(self["quote"].amount / other["quote"].amount), self["quote"]["symbol"],
                dpay_instance=self.dpay
            )
        elif isinstance(other, Amount):
            if not other["asset"] == self["quote"]["asset"]:
                raise AssertionError()
            a = other.copy() / self["price"]
            a["asset"] = self["base"]["asset"].copy()
            a["symbol"] = self["base"]["asset"]["symbol"]
        else:
            a["base"] /= other
        return a

    def __idiv__(self, other):
        if isinstance(other, Price):
            tmp = self / other
            self["base"] = tmp["base"]
            self["quote"] = tmp["quote"]
        else:
            self["base"] /= other
        return self

    def __floordiv__(self, other):
        raise NotImplementedError("This is not possible as the price is a ratio")

    def __ifloordiv__(self, other):
        raise NotImplementedError("This is not possible as the price is a ratio")

    def __lt__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] < other["price"]
        else:
            return self["price"] < float(other or 0)

    def __le__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] <= other["price"]
        else:
            return self["price"] <= float(other or 0)

    def __eq__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] == other["price"]
        else:
            return self["price"] == float(other or 0)

    def __ne__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] != other["price"]
        else:
            return self["price"] != float(other or 0)

    def __ge__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] >= other["price"]
        else:
            return self["price"] >= float(other or 0)

    def __gt__(self, other):
        if isinstance(other, Price):
            self._check_other(other)
            return self["price"] > other["price"]
        else:
            return self["price"] > float(other or 0)

    __truediv__ = __div__
    __truemul__ = __mul__
    __str__ = __repr__

    @property
    def market(self):
        """ Open the corresponding market

            :returns: Instance of :class:`dpaygo.market.Market` for the
                      corresponding pair of assets.
        """
        from .market import Market
        return Market(
            base=self["base"]["asset"],
            quote=self["quote"]["asset"],
            dpay_instance=self.dpay
        )


class Order(Price):
    """ This class inherits :class:`dpaygo.price.Price` but has the ``base``
        and ``quote`` Amounts not only be used to represent the price (as a
        ratio of base and quote) but instead has those amounts represent the
        amounts of an actual order!

        :param dpaygo.dpay.DPay dpay_instance: DPay instance

        .. note::

                If an order is marked as deleted, it will carry the
                'deleted' key which is set to ``True`` and all other
                data be ``None``.
    """
    def __init__(self, base, quote=None, dpay_instance=None, **kwargs):

        self.dpay = dpay_instance or shared_dpay_instance()

        if (
            isinstance(base, dict) and
            "sell_price" in base
        ):
            super(Order, self).__init__(base["sell_price"])
            self["id"] = base.get("id")
        elif (
            isinstance(base, dict) and
            "min_to_receive" in base and
            "amount_to_sell" in base
        ):
            super(Order, self).__init__(
                Amount(base["min_to_receive"], dpay_instance=self.dpay),
                Amount(base["amount_to_sell"], dpay_instance=self.dpay),
            )
            self["id"] = base.get("id")
        elif isinstance(base, Amount) and isinstance(quote, Amount):
            super(Order, self).__init__(None, base=base, quote=quote)
        else:
            raise ValueError("Unknown format to load Order")

    def __repr__(self):
        if "deleted" in self and self["deleted"]:
            return "deleted order %s" % self["id"]
        else:
            t = ""
            if "time" in self and self["time"]:
                t += "(%s) " % self["time"]
            if "type" in self and self["type"]:
                t += "%s " % str(self["type"])
            if "quote" in self and self["quote"]:
                t += "%s " % str(self["quote"])
            if "base" in self and self["base"]:
                t += "%s " % str(self["base"])
            return t + "@ " + Price.__repr__(self)

    __str__ = __repr__


class FilledOrder(Price):
    """ This class inherits :class:`dpaygo.price.Price` but has the ``base``
        and ``quote`` Amounts not only be used to represent the price (as a
        ratio of base and quote) but instead has those amounts represent the
        amounts of an actually filled order!

        :param dpaygo.dpay.DPay dpay_instance: DPay instance

        .. note:: Instances of this class come with an additional ``date`` key
                  that shows when the order has been filled!
    """

    def __init__(self, order, dpay_instance=None, **kwargs):

        self.dpay = dpay_instance or shared_dpay_instance()
        if isinstance(order, dict) and "current_pays" in order and "open_pays" in order:
            # filled orders from account history
            if "op" in order:
                order = order["op"]

            super(FilledOrder, self).__init__(
                Amount(order["open_pays"], dpay_instance=self.dpay),
                Amount(order["current_pays"], dpay_instance=self.dpay),
            )
            if "date" in order:
                self["date"] = formatTimeString(order["date"])

        else:
            raise ValueError("Couldn't parse 'Price'.")

    def json(self):
        return {
            "date": formatTimeString(self["date"]),
            "current_pays": self["base"].json(),
            "open_pays": self["quote"].json(),
        }

    def __repr__(self):
        t = ""
        if "date" in self and self["date"]:
            t += "(%s) " % self["date"]
        if "type" in self and self["type"]:
            t += "%s " % str(self["type"])
        if "quote" in self and self["quote"]:
            t += "%s " % str(self["quote"])
        if "base" in self and self["base"]:
            t += "%s " % str(self["base"])
        return t + "@ " + Price.__repr__(self)

    __str__ = __repr__
