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
  def __init__(self, name: str):
    super().__init__(name=name)
    self.key = 0
  
  # n個のqubitを送信成功するまで，qubitを送り続ける
  ## これbb84_send_appに実装すればいい気がする
  def send_qubits(self, n_until: int):
    bb84_app = self.apps[0]
    while len(bb84_app.succ_key_pool) < n_until:
      bb84_app.send_qubit()

  # 送信成功した量子ビットから鍵を生成
  def obtain_key_from_qbits(self):
    bb84_app = self.apps[0]
    key: int = int("".join(map(str, bb84_app.succ_key_pool.values())), 2) # 10進
    self.key = key

  # 鍵を使って暗号文を作成
  def encrypt(self, message: str) -> int:
    m_bin = int(message.encode().hex(), 16) # 10進
    if len(hex(m_bin)) > len(hex(self.key)):
      raise ValueError("message is bigger than key!")
    cipher: int = m_bin ^ self.key
    return cipher

  # 送信はどうする？
  def send_cipher(self, cipher):
    pass

  # 暗号文をつくって送信
  def encrypt_then_send(self, message: str):
    cipher: int = self.encrypt(message)
    self.send_cipher(cipher)

  # 鍵で復号
  def decrypt(self, cipher: int) -> str:
    m_decimal: int = cipher ^ self.key
    m_hex: str = hex(m_decimal)[2:] # 0x を消すための[2:]
    message: str = bytes.fromhex(m_hex).decode()
    return message


# prepare simulator
## simulate 1 second
#s = Simulator(0, 1, accuracy=10000000000)

# generate quantum nodes
n_send = ComQNode(name="n_send")
n_recv = ComQNode(name="n_recv")

# generate quantum channels and classic channels
qlink = QuantumChannel(
    name="l1", delay=length / light_speed, drop_rate=drop_rate(length)
)
clink = ClassicChannel(name="c1", delay=length / light_speed)

# add channels to the nodes
n_send.add_cchannel(clink)
n_recv.add_cchannel(clink)
n_send.add_qchannel(qlink)
n_recv.add_qchannel(qlink)

# BB84
sp = BB84SendApp(dest=n_recv, qchannel=qlink, cchannel=clink, send_rate=1000)
rp = BB84RecvApp(src=n_send,  qchannel=qlink, cchannel=clink)
n_send.add_apps(sp)
n_recv.add_apps(rp)

# install all nodes
#n1.install(s)
#n2.install(s)

# run the simulation
#s.run()

# share key
n_send.send_qubits(n_until=128) # 128bit
n_send.obtain_key_from_qbits()
n_recv.obtain_key_from_qbits()

# n1: encrypt
message: str = "hello, quantum key deliver!"
n_send.encrypt_then_send(message)
#n_recv.decrypt()

