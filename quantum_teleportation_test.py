from qns.models.epr import BellStateEntanglement
from qns.models.qubit.qubit import Qubit
from qns.models.qubit.const import QUBIT_STATE_0, QUBIT_STATE_1

def exp() -> bool:
  # もつれモデル？の作成 
  e1 = BellStateEntanglement(fidelity=0.8, name="e1")
  #q0, q1 = e1.to_qubits() # もつれ量子対を得ると失敗する

  # 送信したい量子を作成 
  q_sent = Qubit(QUBIT_STATE_0)
	
  # 量子テレポーテーション：結果はq_outに渡される 
  q_out: Qubit = e1.teleportion(q_sent)

  # テレポーテーションが成功したか調べて結果を返す 
  q_sent_prev: int = 0 # q_sent.measure()にすると観測のせいで失敗する
  if q_sent_prev == q_out.measure():
    return True
  return False


# 10000回繰り返してテレポーテーション成功回数を求める
success: int = 0
failure: int = 0
for i in range(10000):
  if exp():
    success += 1
  else:
    failure += 1

print(f"{success=}, {failure=}")
