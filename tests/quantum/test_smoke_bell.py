"""Prueba de humo: verifica que Qiskit y AerSimulator funcionan en el entorno."""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

SHOTS = 1000
SEED = 1234  # semilla fija para que la prueba sea reproducible


def build_bell_circuit() -> QuantumCircuit:
    """Construye el estado de Bell (|00> + |11>) / sqrt(2) y lo mide."""
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)  # superposicion en el qubit 0
    circuit.cx(0, 1)  # entrelaza el qubit 1 con el qubit 0
    circuit.measure([0, 1], [0, 1])
    return circuit


def run_circuit(circuit: QuantumCircuit) -> dict[str, int]:
    """Transpila el circuito para AerSimulator y devuelve los conteos."""
    simulator = AerSimulator()
    compiled = transpile(circuit, simulator)
    job = simulator.run(compiled, shots=SHOTS, seed_simulator=SEED)
    return job.result().get_counts()


def test_bell_state_only_yields_00_and_11() -> None:
    counts = run_circuit(build_bell_circuit())
    # Un estado de Bell nunca debe producir 01 ni 10.
    assert set(counts) <= {"00", "11"}


def test_bell_state_outcomes_are_about_half_each() -> None:
    counts = run_circuit(build_bell_circuit())
    # Cada resultado debe aparecer cerca del 50 % de las veces.
    for outcome in ("00", "11"):
        assert 0.4 < counts.get(outcome, 0) / SHOTS < 0.6
