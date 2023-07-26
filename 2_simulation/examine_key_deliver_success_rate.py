from qns.simulator.simulator import Simulator
from qns.entity.cchannel.cchannel import ClassicChannel
from qns.entity.qchannel.qchannel import QuantumChannel
from qns.entity import QNode
from qns.network.protocol.bb84 import BB84RecvApp, BB84SendApp
import numpy as np

light_speed = 299791458


def drop_rate(length: int) -> float:
  # drop 0.2 db/km
  return 1 - np.exp(-length / 50000)


def simulate_success_rate_by_distance(length: int) -> float:
  simulate_time: int = 100 # second
  qubit_send_rate: int = 1000 # bit/s 

  # prepare simulator
  s = Simulator(0, simulate_time, accuracy=10000000000)

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
  sp = BB84SendApp(n2, qlink, clink, send_rate=qubit_send_rate)
  rp = BB84RecvApp(n1, qlink, clink)
  n1.add_apps(sp)
  n2.add_apps(rp)

  # install all nodes
  n1.install(s)
  n2.install(s)

  # run the simulation
  s.run()

  # BB84RecvApp's succ_key_pool counts the number of success key distribution
  # return parsentage of success to distribute keys
  success_rate: float = len(rp.succ_key_pool) / (simulate_time * qubit_send_rate)
  recv_qubits: int = len(rp.qubit_list)
  qubit_drop_rate: float = drop_rate(length)
  print(f"{length}km:\t{success_rate}\t({recv_qubits=}, {qubit_drop_rate=})")
  return success_rate


# 距離を変えてシミュレーションを行い，鍵配送の成功率を調べる
for dist in [1, 10, 100, 1000, 2000, 5000, 10000, 20000, 50000, 100000, 200000, 500000, 1000000]:
  simulate_success_rate_by_distance(dist)
  #print(f"{dist}km:\t{simulate_success_rate_by_distance(dist)}\t({rp.qubit_list=})")

