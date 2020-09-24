from __future__ import annotations
from dataclasses import dataclass, FrozenInstanceError
from operator import add, sub, mul
from typing import *

BIG_PRIME = 2_147_483_647


@dataclass(frozen=True)
class ModInt:
    val: int
    coprime: int = BIG_PRIME

    def __post_init__(self):
        object.__setattr__(self, "val", self.val % self.coprime)

    def inverse(self) -> ModInt:
        def egcd(x: int, y: int) -> Tuple[int, int, int]:
            if y == 0:
                return (x, 1, 0)
            else:
                d, a, b = egcd(y, x % y)  # d = ax + by
                return (d, b, a - (x // y) * b)

        return ModInt(egcd(self.coprime, self.val)[2], coprime=self.coprime)

    def _gen_operation(
        int_op: Callable[[int, int], int], name: str
    ) -> Callable[[ModInt, Union[ModInt, int]], ModInt]:
        def operation(self: ModInt, other: Union[ModInt, int]) -> ModInt:
            if isinstance(other, int):
                return ModInt(
                    int_op(self.val, other % self.coprime) % self.coprime, self.coprime
                )
            elif isinstance(other, ModInt) and other.coprime == self.coprime:
                return ModInt(int_op(self.val, other.val) % self.coprime, self.coprime)
            elif other.coprime != self.coprime:
                raise ValueError(
                    f"Different coprime moduli in {name}: {self.coprime}, {other.coprime}."
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

    def __truediv__(self, other: Union[ModInt, int]) -> ModInt:
        if isinstance(other, int):
            other = ModInt(other, self.coprime)
        return self * other.inverse()

    __rtruediv__ = __truediv__

    def __pow__(self, power: int) -> ModInt:
        result = ModInt(1, self.coprime)
        if power < 0:
            result, power = self.inverse(), -power - 1
            self = result

        while power > 0:
            if power % 2 == 1:
                result = result * self
            self, power = self * self, power // 2

        return result

    def __repr__(self):
        return f"ModInt(val={self.val}, coprime={self.coprime})"

    def __str__(self):
        return f"{self.val} (mod {self.coprime})"
