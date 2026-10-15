"""Tests de las compuertas de multiplicacion modular."""

import pytest
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from shor_vs_rsa.quantum.modular_mult import multiply_by_7, negate, rotate_right

QUBITS = [0, 1, 2, 3]


def apply_gate(gate, y: int) -> int:
    """Aplica la compuerta al estado |y> y devuelve el entero resultante."""
    circuit = QuantumCircuit(4)
    gate(circuit, QUBITS)
    final_state = Statevector.from_int(y, 16).evolve(circuit)
    # Un estado base se mapea a otro estado base, asi que hay una sola clave.
    (bitstring,) = final_state.probabilities_dict().keys()
    return int(bitstring, 2)


def rotate_right_classical(y: int) -> int:
    """Referencia clasica: el bit menos significativo pasa al mas significativo."""
    return ((y & 1) << 3) | (y >> 1)


@pytest.mark.parametrize("y", range(16))
def test_rotate_right_matches_classical_rotation(y: int) -> None:
    assert apply_gate(rotate_right, y) == rotate_right_classical(y)


@pytest.mark.parametrize("y", range(16))
def test_negate_flips_every_bit(y: int) -> None:
    assert apply_gate(negate, y) == 15 - y


@pytest.mark.parametrize("y", range(1, 15))
def test_multiply_by_7_matches_modular_arithmetic(y: int) -> None:
    assert apply_gate(multiply_by_7, y) == (7 * y) % 15


def test_multiply_by_7_follows_the_cycle_of_the_order() -> None:
    # El ciclo de potencias de 7 modulo 15: 1 -> 7 -> 4 -> 13 -> 1
    y = 1
    visited = []
    for _ in range(4):
        y = apply_gate(multiply_by_7, y)
        visited.append(y)
    assert visited == [7, 4, 13, 1]


@pytest.mark.parametrize(("y", "expected"), [(0, 15), (15, 0)])
def test_multiply_by_7_swaps_zero_and_fifteen(y: int, expected: int) -> None:
    # Limitacion documentada: 0 y 15 se intercambian (ver docstring del modulo).
    assert apply_gate(multiply_by_7, y) == expected


@pytest.mark.parametrize("gate", [rotate_right, negate, multiply_by_7])
def test_wrong_number_of_qubits_raises_value_error(gate) -> None:
    with pytest.raises(ValueError):
        gate(QuantumCircuit(3), [0, 1, 2])
