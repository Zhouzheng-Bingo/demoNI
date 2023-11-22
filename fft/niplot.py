import nidaqmx
import pprint
import numpy as np
from matplotlib import pyplot as plt

from scipy.fftpack import fft, ifft

from matplotlib.pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
mpl.rcParams['axes.unicode_minus'] = False  # 显示负号
N=1500  #频率
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev1/ai1")
    task.timing.cfg_samp_clk_timing(
        rate=600,
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
        samps_per_chan=10000
    )

    data = task.read(number_of_samples_per_channel=N)
    x=np.arange(0,N) #频率个数
    fft_data = fft(data)   #傅里叶变换
    half_x = x[range(int(N/2))] #一半的画图就行
    abs_y = np.abs(fft_data)  # 取复数的绝对值，即复数的模(双边频谱)
    angle_y = np.angle(fft_data)  # 取复数的角度
    normalization_y = abs_y / N  # 归一化处理（双边频谱）
    normalization_half_y = normalization_y[range(int(N / 2))]  # 由于对称性，只取一半区间（单边频谱）

    plt.subplot(231)
    plt.plot(x, data)
    plt.title('原始数据')

    plt.subplot(232)
    plt.plot(x, fft_data, 'black')
    plt.title('双边振幅谱(未求振幅绝对值)', fontsize=9, color='black')

    plt.subplot(233)
    plt.plot(x, abs_y, 'r')
    plt.title('双边振幅谱(未归一化)', fontsize=9, color='red')

    plt.subplot(234)
    plt.plot(x, angle_y, 'violet')
    plt.title('双边相位谱(未归一化)', fontsize=9, color='violet')

    plt.subplot(235)
    plt.plot(x, normalization_y, 'g')
    plt.title('双边振幅谱(归一化)', fontsize=9, color='green')

    plt.subplot(236)
    plt.plot(half_x, normalization_half_y, 'blue')
    plt.title('单边振幅谱(归一化)', fontsize=9, color='blue')

    plt.show()
