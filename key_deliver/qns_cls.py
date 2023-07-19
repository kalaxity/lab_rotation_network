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


# prepare simulator
s = Simulator(0, 10, accuracy=10000000000)

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

# BB84RecvApp's succ_key_pool counts the number of success key distribution
# the rate is succ_key_pool/ simulation_time (10s)
print("success_:", len(rp.succ_key_pool) / 10)

