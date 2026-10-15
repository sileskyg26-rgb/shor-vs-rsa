"""Busqueda clasica del orden multiplicativo de a modulo n."""

from math import gcd
from typing import Protocol


class OrderFinder(Protocol):
    """Interfaz minima: cualquier objeto que sepa encontrar el orden de a modulo n.

    La version clasica (fuerza bruta) y la cuantica (Shor) la cumpliran,
    asi el resto del codigo puede usar cualquiera de las dos.
    """

    def find_order(self, a: int, n: int) -> int: ...


class BruteForceOrderFinder:
    """Encuentra el orden probando potencias de a una por una."""

    def find_order(self, a: int, n: int) -> int:
        """Devuelve el menor r > 0 tal que a^r = 1 (mod n).

        Lanza ValueError si n < 2 o si a no es coprimo con n,
        porque en ese caso el orden no existe.
        """
        self._validate(a, n)

        value = a % n  # a^1 mod n
        order = 1
        while value != 1:
            value = (value * a) % n  # pasa de a^k a a^(k+1)
            order += 1
        return order

    @staticmethod
    def _validate(a: int, n: int) -> None:
        if n < 2:
            raise ValueError(f"n debe ser al menos 2, se recibio {n}")
        if gcd(a, n) != 1:
            # Si gcd(a, n) > 1, las potencias de a nunca llegan a 1 modulo n.
            raise ValueError(f"a={a} y n={n} no son coprimos; el orden no existe")
