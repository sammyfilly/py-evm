import decimal
import functools
import itertools
from typing import (
    Union,
)

from eth_typing import (
    Hash32,
)
from eth_utils.toolz import (
    curry,
)

from eth.constants import (
    UINT_255_MAX,
    UINT_256_CEILING,
    UINT_256_MAX,
)


def int_to_bytes32(value: Union[int, bool]) -> Hash32:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"Value must be an integer: Got: {type(value)}")
    if value < 0:
        raise ValueError(f"Value cannot be negative: Got: {value}")
    if value > UINT_256_MAX:
        raise ValueError(f"Value exeeds maximum UINT256 size.  Got: {value}")
    value_bytes = value.to_bytes(32, "big")
    return Hash32(value_bytes)


def ceilXX(value: int, ceiling: int) -> int:
    remainder = value % ceiling
    return value if remainder == 0 else value + ceiling - remainder


ceil32 = functools.partial(ceilXX, ceiling=32)
ceil8 = functools.partial(ceilXX, ceiling=8)


def unsigned_to_signed(value: int) -> int:
    return value if value <= UINT_255_MAX else value - UINT_256_CEILING


def signed_to_unsigned(value: int) -> int:
    return value + UINT_256_CEILING if value < 0 else value


def is_even(value: int) -> bool:
    return value % 2 == 0


def is_odd(value: int) -> bool:
    return value % 2 == 1


def get_highest_bit_index(value: int) -> int:
    value >>= 1
    for bit_length in itertools.count():
        if not value:
            return bit_length
        value >>= 1

    raise Exception("Invariant: unreachable code path")


@curry
def clamp(inclusive_lower_bound: int, inclusive_upper_bound: int, value: int) -> int:
    """
    Bound the given ``value`` between ``inclusive_lower_bound`` and
    ``inclusive_upper_bound``.
    """
    if value <= inclusive_lower_bound:
        return inclusive_lower_bound
    elif value >= inclusive_upper_bound:
        return inclusive_upper_bound
    else:
        return value


def integer_squareroot(value: int) -> int:
    """
    Return the integer square root of ``value``.

    Uses Python's decimal module to compute the square root of ``value`` with
    a precision of 128-bits. The value 128 is chosen since the largest square
    root of a 256-bit integer is a 128-bit integer.
    """
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"Value must be an integer: Got: {type(value)}")
    if value < 0:
        raise ValueError(f"Value cannot be negative: Got: {value}")

    with decimal.localcontext() as ctx:
        ctx.prec = 128
        return int(decimal.Decimal(value).sqrt())
