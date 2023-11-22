import nidaqmx
from nidaqmx.constants import LineGrouping

#开始一个任务
# with nidaqmx.Task() as task:
#      task.ai_channels.add_ai_voltage_chan("Dev1/ai0:3")
#      data = task.read()
#      print(type(data))
#      for da in data:
#          print(da)


# with nidaqmx.Task() as task:
#     task.di_channels.add_di_chan(
#         "cDAQ2Mod4/port0/line0:1",
#         line_grouping=LineGrouping.CHAN_PER_LINE
#     )
#     task.read(number_of_samples_per_channel=2)

# from nidaqmx.types import CtrTime
# with nidaqmx.Task() as task:
#     task.co_channels.add_co_pulse_chan_time("Dev1/ctr0")
#     sample = CtrTime(high_time=0.001, low_time=0.001)
#     task.write(sample)
import nidaqmx
import pprint
import numpy as np
from matplotlib import pyplot as plt

pp = pprint.PrettyPrinter(indent=4)


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0:4")

    # print('1 Channel 1 Sample Read: ')
    data = task.read()
    pp.pprint(data)

    # data = task.read(number_of_samples_per_channel=1)
    # pp.pprint(data)
    #
    # print('1 Channel N Samples Read: ')
    # data = task.read(number_of_samples_per_channel=10)
    # x=np.arange(0,len(data))
    # pp.pprint(data)
    # plt.plot(x,data)
    # plt.show()
    #
    # task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
    #
    # print('N Channel 1 Sample Read: ')
    # data = task.read()
    # pp.pprint(data)
    #
    # print('N Channel N Samples Read: ')
    # data = task.read(number_of_samples_per_channel=2)
    # pp.pprint(data)