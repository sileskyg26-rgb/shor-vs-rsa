"""Tests del paso de recuperacion de factores a partir del orden."""

import pytest

from shor_vs_rsa.classical.factor_recovery import factors_from_order


def test_a7_r4_recovers_3_and_5() -> None:
    # gcd(7^2 - 1, 15) = gcd(48, 15) = 3 y gcd(7^2 + 1, 15) = gcd(50, 15) = 5
    assert factors_from_order(7, 15, 4) == (3, 5)


@pytest.mark.parametrize(("a", "r"), [(2, 4), (4, 2), (8, 4), (11, 2), (13, 4)])
def test_other_valid_pairs_mod_15(a: int, r: int) -> None:
    assert factors_from_order(a, 15, r) == (3, 5)


def test_r2_for_a7_fails_because_it_is_not_the_period() -> None:
    # Es el caso de la fase 1/2: 7^2 = 4 (mod 15), asi que r = 2 es falso.
    assert factors_from_order(7, 15, 2) is None


def test_odd_order_returns_none() -> None:
    # a = 1 tiene orden 1 (impar): no se puede dividir entre 2.
    assert factors_from_order(1, 15, 1) is None


def test_half_power_equal_to_minus_one_returns_none() -> None:
    # 14^1 = -1 (mod 15), el caso malo a^(r/2) = -1.
    assert factors_from_order(14, 15, 2) is None


def test_multiple_of_the_order_with_trivial_factor_returns_none() -> None:
    # r = 8 cumple 7^8 = 1, pero 7^4 = 1 y gcd(0, 15) = 15 (factor trivial).
    assert factors_from_order(7, 15, 8) is None


def test_works_for_another_modulus() -> None:
    # 2 tiene orden 6 modulo 21; 2^3 = 8 y gcd(7, 21) = 7.
    assert factors_from_order(2, 21, 6) == (3, 7)


def test_result_multiplies_back_to_n() -> None:
    factors = factors_from_order(7, 15, 4)
    assert factors is not None
    assert factors[0] * factors[1] == 15


@pytest.mark.parametrize("n", [1, 0, -15])
def test_modulus_below_two_raises_value_error(n: int) -> None:
    with pytest.raises(ValueError):
        factors_from_order(7, n, 4)


@pytest.mark.parametrize("r", [0, -4])
def test_non_positive_order_raises_value_error(r: int) -> None:
    with pytest.raises(ValueError):
        factors_from_order(7, 15, r)
