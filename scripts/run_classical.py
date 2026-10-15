"""Muestra la parte clasica de Shor para N = 15, a = 7 (sin circuito cuantico)."""

from math import gcd

from shor_vs_rsa.classical.factor_recovery import factors_from_order
from shor_vs_rsa.classical.order_finding import BruteForceOrderFinder

N = 15
A = 7


def main() -> None:
    # Potencias de a modulo N hasta volver a 1 (es la secuencia que define el orden).
    order = BruteForceOrderFinder().find_order(A, N)
    powers = [pow(A, k, N) for k in range(1, order + 1)]
    print(f"Potencias de {A} modulo {N}: {powers}")
    print(f"Orden r = {order}")

    factors = factors_from_order(A, N, order)
    if factors is None:
        print("Este r no permite factorizar; habria que probar otro a.")
        return
    half = pow(A, order // 2)
    print(f"gcd({A}^{order // 2} - 1, {N}) = gcd({half - 1}, {N}) = {gcd(half - 1, N)}")
    print(f"gcd({A}^{order // 2} + 1, {N}) = gcd({half + 1}, {N}) = {gcd(half + 1, N)}")
    print(f"Factores de {N}: {factors[0]} x {factors[1]}")


if __name__ == "__main__":
    main()
