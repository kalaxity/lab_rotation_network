from qns.models.epr import BellStateEntanglement
from qns.models.qubit.qubit import Qubit
from qns.models.qubit.const import QUBIT_STATE_0, QUBIT_STATE_1

e1 = BellStateEntanglement(fidelity=0.8, name="e1")

# change BellStateEntanglement model to Qubit model
q0, q1 = e1.to_qubits()
print("prev_q0:", q0.state)
print("prev_q1:", q1.state)

# execute teleportation protocol to transmit a Qubit
q0 = Qubit(QUBIT_STATE_1) # the transmitting qubit
e1 = BellStateEntanglement(fidelity=0.8, name="e0")
print("q0:", q0.state)
print("q1:", q1.state)

q2: Qubit = e1.teleportion(q0) # The transmitted qubit
print("q2:", q2.measure())
print(q0.measure(), q1.measure())
