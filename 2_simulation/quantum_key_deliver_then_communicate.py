from qns.simulator.simulator import Simulator
from qns.entity.cchannel.cchannel import ClassicChannel
from qns.entity.qchannel.qchannel import QuantumChannel
from qns.entity import QNode
from qns.network.protocol.bb84 import BB84RecvApp, BB84SendApp
import numpy as np

light_speed = 299791458
length = 100000  # 100,000 km


def drop_rate(length):
  # drop 0.2 db/KM
  return 1 - np.exp(-length / 50000)


# 鍵共有，平文の暗号化が可能なQNode
class ComQNode(QNode):
  def __init__(self):
    super().__init__()
    self.key = 0b0 # 2進数の0
  
  # n個のqubitを送信成功するまで，qubitを送り続ける
  ## これbb84_send_appに実装すればいい気がする
  #def send_qbits(n: int):
  #  bb84_app = self.apps[0]
  #  while len(bb84_app.succ_key_pool) < n:
  #    bb84_app.send_qubit()

  # 送信成功した量子ビットから鍵を生成
  def obtain_key_from_qbits():
    bb84_app = self.apps[0]
    key: int = int("".join(map(str, bb84_app.succ_key_pool.values())), 2)
    self.key = key

  # 鍵を使って暗号文を作成
  def encrypt(message: str) -> str:
    pass # ここでバーナム暗号！

  # 送信はどうする？

  # 鍵で復号
  def decrypt(cipher: str) -> str:
    pass 


# prepare simulator
## simulate 1 second
s = Simulator(0, 1, accuracy=10000000000)

# generate quantum nodes
n1 = QNode(name="n1")
n2 = QNode(name="n2")

# generate quantum channels and classic channels
qlink = QuantumChannel(
    name="l1", delay=length / light_speed, drop_rate=drop_rate(length)
)
clink = ClassicChannel(name="c1", delay=length / light_speed)

# add channels to the nodes
n1.add_cchannel(clink)
n2.add_cchannel(clink)
n1.add_qchannel(qlink)
n2.add_qchannel(qlink)

# BB84
sp = BB84SendApp(n2, qlink, clink, send_rate=1000)
rp = BB84RecvApp(n1, qlink, clink)
n1.add_apps(sp)
n2.add_apps(rp)

# install all nodes
n1.install(s)
n2.install(s)

# run the simulation
s.run()

# key
key = int("".join(map(str, rp.succ_key_pool.values())), 2)
n1.key = key
n2.key = key

# n1: encrypt
message: str = "hello, quantum key deliver!"

