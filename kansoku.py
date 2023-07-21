# 観測することで状態が変わってしまうことを示す
from qns.models.qubit.qubit import Qubit
from qns.models.qubit.const import QUBIT_STATE_P

q = Qubit(QUBIT_STATE_P)
print("state of q:", q.state)
print("measure q:", q.measure())
print("state of q:", q.state)
