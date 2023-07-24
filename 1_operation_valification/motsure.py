# 量子もつれが機能していることを確認します

from qns.models.epr import BellStateEntanglement
from qns.models.qubit.qubit import Qubit

# 量子もつれを生成
e1 = BellStateEntanglement(fidelity=0.8, name="e1")
# そこからもつれ量子ペア(q0, q1)を取り出す
q0, q1 = e1.to_qubits()

# q1の状態を調べる
print(f"confirm the state of q1\n{q1.state}\n")

# q0を観測してから，再度q1の状態を調べる
print(f"measure q0 and the result is: {q0.measure()}\n")
print(f"re-confirm the state of q1\n{q1.state}") # q0を観測するとq1のstateが変わる

