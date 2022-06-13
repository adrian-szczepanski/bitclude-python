# -*- coding: utf-8 -*-

"""CCXT: CryptoCurrency eXchange Trading Library (Async)"""

# -----------------------------------------------------------------------------

__version__ = '1.30.51'

# -----------------------------------------------------------------------------

from ccxt_bitclude.async_support.base.exchange import Exchange                   # noqa: F401

from ccxt_bitclude.base.decimal_to_precision import decimal_to_precision  # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import TRUNCATE              # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import ROUND                 # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import DECIMAL_PLACES        # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import SIGNIFICANT_DIGITS    # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import NO_PADDING            # noqa: F401
from ccxt_bitclude.base.decimal_to_precision import PAD_WITH_ZERO         # noqa: F401

from ccxt_bitclude.base import errors                                # noqa: F401
from ccxt_bitclude.base.errors import BaseError                      # noqa: F401
from ccxt_bitclude.base.errors import ExchangeError                  # noqa: F401
from ccxt_bitclude.base.errors import AuthenticationError            # noqa: F401
from ccxt_bitclude.base.errors import PermissionDenied               # noqa: F401
from ccxt_bitclude.base.errors import AccountSuspended               # noqa: F401
from ccxt_bitclude.base.errors import ArgumentsRequired              # noqa: F401
from ccxt_bitclude.base.errors import BadRequest                     # noqa: F401
from ccxt_bitclude.base.errors import BadSymbol                      # noqa: F401
from ccxt_bitclude.base.errors import BadResponse                    # noqa: F401
from ccxt_bitclude.base.errors import NullResponse                   # noqa: F401
from ccxt_bitclude.base.errors import InsufficientFunds              # noqa: F401
from ccxt_bitclude.base.errors import InvalidAddress                 # noqa: F401
from ccxt_bitclude.base.errors import AddressPending                 # noqa: F401
from ccxt_bitclude.base.errors import InvalidOrder                   # noqa: F401
from ccxt_bitclude.base.errors import OrderNotFound                  # noqa: F401
from ccxt_bitclude.base.errors import OrderNotCached                 # noqa: F401
from ccxt_bitclude.base.errors import CancelPending                  # noqa: F401
from ccxt_bitclude.base.errors import OrderImmediatelyFillable       # noqa: F401
from ccxt_bitclude.base.errors import OrderNotFillable               # noqa: F401
from ccxt_bitclude.base.errors import DuplicateOrderId               # noqa: F401
from ccxt_bitclude.base.errors import NotSupported                   # noqa: F401
from ccxt_bitclude.base.errors import NetworkError                   # noqa: F401
from ccxt_bitclude.base.errors import DDoSProtection                 # noqa: F401
from ccxt_bitclude.base.errors import RateLimitExceeded              # noqa: F401
from ccxt_bitclude.base.errors import ExchangeNotAvailable           # noqa: F401
from ccxt_bitclude.base.errors import OnMaintenance                  # noqa: F401
from ccxt_bitclude.base.errors import InvalidNonce                   # noqa: F401
from ccxt_bitclude.base.errors import RequestTimeout                 # noqa: F401
from ccxt_bitclude.base.errors import error_hierarchy                # noqa: F401


from ccxt_bitclude.async_support.bitclude import bitclude                          # noqa: F401

exchanges = [
    'bitclude',
]

base = [
    'Exchange',
    'exchanges',
    'decimal_to_precision',
]

__all__ = base + errors.__all__ + exchanges
