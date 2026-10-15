"""Tests de la busqueda clasica del orden."""

import pytest

from shor_vs_rsa.classical.order_finding import BruteForceOrderFinder, OrderFinder

finder = BruteForceOrderFinder()


def test_order_of_7_mod_15_is_4() -> None:
    # Potencias de 7 modulo 15: 7, 4, 13, 1
    assert finder.find_order(7, 15) == 4


@pytest.mark.parametrize(
    ("a", "expected_order"),
    [(1, 1), (2, 4), (4, 2), (7, 4), (8, 4), (11, 2), (13, 4), (14, 2)],
)
def test_orders_for_every_unit_mod_15(a: int, expected_order: int) -> None:
    assert finder.find_order(a, 15) == expected_order


@pytest.mark.parametrize("a", [7, 2, 11])
def test_order_is_the_smallest_power_that_gives_one(a: int) -> None:
    order = finder.find_order(a, 15)
    assert pow(a, order, 15) == 1
    # Ninguna potencia menor debe dar 1.
    assert all(pow(a, k, 15) != 1 for k in range(1, order))


@pytest.mark.parametrize("a", [3, 5, 6, 9, 10, 12])
def test_non_coprime_a_raises_value_error(a: int) -> None:
    with pytest.raises(ValueError):
        finder.find_order(a, 15)


@pytest.mark.parametrize("n", [1, 0, -15])
def test_modulus_below_two_raises_value_error(n: int) -> None:
    with pytest.raises(ValueError):
        finder.find_order(7, n)


def test_brute_force_finder_satisfies_the_order_finder_interface() -> None:
    # Comprobacion de tipos: la clase puede usarse donde se espera un OrderFinder.
    usable: OrderFinder = BruteForceOrderFinder()
    assert usable.find_order(7, 15) == 4
