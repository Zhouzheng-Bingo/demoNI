# ----------- client 端 -----------
import asyncio

import nidaqmx
import websockets

async def getdatalist(chann,num):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"Dev1/ai{chann}")
        task.timing.cfg_samp_clk_timing(
            rate=200,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=40000
        )

        datalist = task.read(number_of_samples_per_channel=num)
        return datalist
async def getdatalist2(num):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"Dev1/ai0:1")
        task.timing.cfg_samp_clk_timing(
            rate=200,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=40000
        )

        datalist = task.read(number_of_samples_per_channel=num)
        return datalist
async def send_msg1(websocket,chann):
    i = 0
    while True:
        try:
            datalist = await getdatalist(chann,100)
            print(f"-------start!! {i} !!send data to server!----")
            for data in datalist:
                await websocket.send(str(chann)+"|"+str(data))
                # print(f"---->have send the data : {data}")
                rec_str = await websocket.recv()
                print(f"***** 通道 {chann} 的数据已发送 : {rec_str}")

            print("-------send    finished!----\n\n")
            i += 1
            await asyncio.sleep(2)
        except websockets.ConnectionClosedError:
            print("服务器已关闭")
            print(f"共发送{i*100}条数据")
            return True

#读两条ai0 ai1 的值
async def send_msg2(websocket):
    i = 0
    while True:
        try:
            datalist = await getdatalist2(100)
            print(f"-------start!! {i} !!send data to server!----")
            for i in range(100):
                await websocket.send(str(datalist[0][i])+"|"+str(datalist[1][i]))
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

async def main_logic(chann):

    async with websockets.connect('ws://localhost:8765') as websocket:
        # await send_msg2()
        await send_msg1(websocket,chann=chann)
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