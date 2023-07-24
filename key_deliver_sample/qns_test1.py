from qns.simulator.simulator import Simulator
from qns.entity.cchannel.cchannel import ClassicChannel
from qns.entity import QNode
import numpy as np

light_speed = 299791458
length = 100000  # 100000km

# prepare simulator
s = Simulator(0, 10, accuracy=10000000000)

# nodes
n1 = QNode(name="n1")
n2 = QNode(name="n2")

# channel
clink = ClassicChannel(name="c1", delay=length / light_speed)
n1.add_cchannel(clink)
n2.add_cchannel(clink)


# install all nodes
n1.install(s)
n2.install(s)

s.run()

print("result")
