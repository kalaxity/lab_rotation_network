# 量子もつれが機能していることを確認
from qns.models.epr import BellStateEntanglement
from qns.models.qubit.qubit import Qubit
from qns.models.qubit.const import QUBIT_STATE_0

e1 = BellStateEntanglement(fidelity=0.8, name="e1")
q0, q1 = e1.to_qubits()

print("state of q1")
print(q1.state)

print("q0.measure =",q0.measure())
print("state of q1")
print(q1.state) # q0を観測するとq1のstateが変わる
