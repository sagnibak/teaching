from __future__ import annotations
from dataclasses import FrozenInstanceError
from operator import add, sub, mul
from typing import *

BIG_PRIME = 2_147_483_647


class ModInt:
    def __init__(self, val: int, prime: int = BIG_PRIME) -> None:
        self.val = val % prime
        self.prime = prime

    def inverse(self) -> ModInt:
        return ModInt(0)
    
    def __setattr__(self, attr, val) -> None:
        raise FrozenInstanceError()

    def __delattr__(self, _) -> None:
        raise FrozenInstanceError()

    def _gen_operation(
        int_op: Callable[[int, int], int], name: str
    ) -> Callable[[ModInt, Union[ModInt, int]], ModInt]:
        def operation(self: ModInt, other: Union[ModInt, int]) -> ModInt:
            if isinstance(other, int):
                return ModInt(
                    int_op(self.val, other % self.prime) % self.prime, self.prime
                )
            elif isinstance(other, ModInt) and other.prime == self.prime:
                return ModInt(int_op(self.val, other.val) % self.prime, self.prime)
            elif other.prime != self.prime:
                raise ValueError(
                    f"Different prime moduli in {name}: {self.prime}, {other.prime}."
                )
            else:
                raise TypeError(f"{name} not defined for {type(other)} and ModInt.")

        return operation

    __add__ = _gen_operation(add, "addition")
    __radd__ = __add__
    __sub__ = _gen_operation(sub, "subtraction")
    __rsub__ = __sub__
    __mul__ = _gen_operation(mul, "multiplication")
    __rmul__ = __mul__

    def __str__(self):
        return f"{self.val} (mod {self.prime})"
