# ----------- client 端 -----------
import asyncio
import numpy as np
import nidaqmx
import websockets


# 这里的采样频率是800Hz，根据设备和采样条件可能需要调整
SAMPLE_RATE = 800
DOWNSAMPLE_FACTOR = 10  # 降采样因子，每10个点取一个
KEY_FREQS = [400]  # 感兴趣的关键频率，需要根据你的设备和条件调整

async def getdatalist2(num):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"Dev1/ai0")
        task.timing.cfg_samp_clk_timing(
            rate=800,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=40000
        )

        datalist = task.read(number_of_samples_per_channel=num)
        print(datalist)
        # 提取关键频率的振幅
        key_amplitudes = []
        # 对每个通道的数据做FFT和降采样


            # FFT
        freqs = np.fft.fftfreq(len(datalist), 1 / SAMPLE_RATE)
        fft_results = np.abs(np.fft.fft(datalist))


        for freq in KEY_FREQS:
            idx = np.argmin(np.abs(freqs - freq))
            key_amplitudes.append(fft_results[idx])

            # 降采样
        key_amplitudes = key_amplitudes[::DOWNSAMPLE_FACTOR]

            # 将处理后的数据存回datalist
        datalist[i] = key_amplitudes

        return datalist


# 读两条ai0 ai1 ai2 的值
async def send_msg2(websocket):
    i = 0
    while True:
        try:
            datalist = await getdatalist2(400)
            print(datalist)
            print(f"-------start!! {i} !!send data to server!----")
            for i in range(100):
                # await websocket.send(str(datalist[0][i]) + "|" + str(datalist[1][i]))
                data = "|".join([str(datalist[j][i]) for j in range(len(datalist))])
                await websocket.send(data)
                # print(f"---->have send the data : {data}")
                rec_str = await websocket.recv()
                print(f"***** 通道的数据已发送 : {rec_str}")

            print("-------send    finished!----\n\n")
            i += 1
            await asyncio.sleep(2)
        except websockets.ConnectionClosedError:
            print("服务器已关闭")
            # print(f"共发送{i*100}条数据")
            return True


async def main_logic2():
    async with websockets.connect('ws://localhost:8765') as websocket:
        # await send_msg2()
        await send_msg2(websocket)


# 多个客户端一起 直插入一个物理通道的值
# loop = asyncio.get_event_loop()
# tasks = [main_logic(i) for i in range(2)]
# loop.run_until_complete(asyncio.wait(tasks))
# 插入ai0 ai1 的值
asyncio.get_event_loop().run_until_complete(main_logic2())