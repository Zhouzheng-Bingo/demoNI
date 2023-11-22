import nidaqmx
import pprint
import numpy as np
from matplotlib import pyplot as plt

pp = pprint.PrettyPrinter(indent=4)


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai0")
    task.timing.cfg_samp_clk_timing(
        rate=200,
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
        samps_per_chan=10000
    )

    # print('1 Channel 1 Sample Read: ')
    # data = task.read()
    # pp.pprint(data)

    # data = task.read(number_of_samples_per_channel=1)
    # pp.pprint(data)
    #
    # print('1 Channel N Samples Read: ')
    data = task.read(number_of_samples_per_channel=1000)
    x=np.arange(0,len(data))
    pp.pprint(data)
    plt.plot(x,data)
    plt.show()
    #

    # task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
    #通道的名字
    # name = task.channel_names
    # print(name)

    #获取通道数量
    # num = task.number_of_channels

    # print('N Channel 1 Sample Read: ')
    # data = task.read()
    # pp.pprint(data)
    #
    # print('N Channel N Samples Read: ')
    # data = task.read(number_of_samples_per_channel=1)
    # pp.pprint(data)