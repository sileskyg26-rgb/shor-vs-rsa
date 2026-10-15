"""Compuertas que multiplican por 7 modulo 15 sobre un registro de 4 qubits.

El registro se lee como un entero con el qubit 0 como bit menos significativo
(convencion de Qiskit): el estado |y> tiene y = q0 + 2*q1 + 4*q2 + 8*q3.
"""

from collections.abc import Sequence

from qiskit import QuantumCircuit

REGISTER_SIZE = 4  # 4 bits representan los enteros 0..15


def _check_size(qubits: Sequence[int]) -> None:
    if len(qubits) != REGISTER_SIZE:
        raise ValueError(f"Se esperaban {REGISTER_SIZE} qubits, se recibieron {len(qubits)}")


def rotate_right(circuit: QuantumCircuit, qubits: Sequence[int]) -> None:
    """Rota los 4 bits una posicion a la derecha (el bit 0 pasa al bit 3).

    Como 16 = 1 (mod 15), esto equivale a multiplicar por 8 modulo 15.
    """
    _check_size(qubits)
    # Tres SWAP vecinos llevan el valor del primer qubit hasta el ultimo
    # y desplazan los demas una posicion hacia abajo.
    for low, high in zip(qubits, qubits[1:]):
        circuit.swap(low, high)


def negate(circuit: QuantumCircuit, qubits: Sequence[int]) -> None:
    """Niega los 4 bits: y pasa a 15 - y."""
    _check_size(qubits)
    for qubit in qubits:
        circuit.x(qubit)


def multiply_by_7(circuit: QuantumCircuit, qubits: Sequence[int]) -> None:
    """Lleva |y> a |7*y mod 15> para y = 1..14.

    Se usa que 7 = -8 (mod 15): primero se multiplica por 8 (rotar) y luego
    se toma el opuesto 15 - x (negar los bits).

    Caso especial: |0> y |15> se intercambian (0 -> 15 y 15 -> 0). Son el mismo
    residuo modulo 15 pero estados distintos del registro. No afecta a Shor,
    porque el ciclo 1 -> 7 -> 4 -> 13 -> 1 nunca pasa por ellos.
    """
    rotate_right(circuit, qubits)
    negate(circuit, qubits)
