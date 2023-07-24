# 観測することで状態が変わってしまうことを示す
from qns.models.qubit.qubit import Qubit
from qns.models.qubit.const import QUBIT_STATE_P

q = Qubit(QUBIT_STATE_P)
print(f"confirm the state of q: \n{q.state}\n")
print(f"measure q and the result is: {q.measure()}\n")
print(f"then, re-confirm the state of q:\n{q.state}")
