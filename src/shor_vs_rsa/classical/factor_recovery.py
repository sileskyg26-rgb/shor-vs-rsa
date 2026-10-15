"""Paso final de Shor: del orden r de a modulo n a los factores de n."""

from math import gcd


def factors_from_order(a: int, n: int, r: int) -> tuple[int, int] | None:
    """Intenta factorizar n usando el orden r de a modulo n.

    Devuelve (p, q) con p <= q y p * q == n, o None si este r no sirve.
    Lanza ValueError si n < 2 o r < 1.
    """
    if n < 2:
        raise ValueError(f"n debe ser al menos 2, se recibio {n}")
    if r < 1:
        raise ValueError(f"r debe ser positivo, se recibio {r}")

    # r tiene que ser un periodo de verdad: a^r = 1 (mod n).
    # Con la fase 1/2 el circuito cuantico propone r = 2, pero 7^2 = 4 (mod 15).
    if pow(a, r, n) != 1:
        return None

    # El truco necesita dividir r entre 2.
    if r % 2 != 0:
        return None

    half = pow(a, r // 2, n)  # a^(r/2) mod n

    # Si a^(r/2) = -1 (mod n), n divide a (a^(r/2) + 1) y el gcd solo da n.
    if half == n - 1:
        return None

    # n divide a (half - 1)(half + 1) pero no a cada factor por separado,
    # asi que gcd(half - 1, n) comparte con n un divisor propio.
    p = gcd(half - 1, n)
    if p in (1, n):
        return None  # factor trivial: no se aprendio nada

    q = n // p
    return (min(p, q), max(p, q))
