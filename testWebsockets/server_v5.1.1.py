# ----------- server 端 -----------
# 三个通道降采样
import asyncio
import websockets

def process_channel_data(channel_data, sensitivity):
    volt = float(channel_data)
    acc = volt / sensitivity
    return acc

async def startServer(websocket, path):
    print('-------- server start ------')
    sens1 = 101.6
    sens2 = 100.0
    sens3 = 99.7
    i = 0
    while True:
        try:
            rec_data = await websocket.recv()
            split_data = rec_data.split("|")
            i += 1

            acc_ch1 = process_channel_data(split_data[0], sens1)
            acc_ch2 = process_channel_data(split_data[1], sens2)
            acc_ch3 = process_channel_data(split_data[2], sens3)

            greeting = "i=" + str(i) + ", server received, not used"

            # 降采样,每10个数据点选取一个
            if i % 10 == 0:
                greeting = f'server get ch1: {acc_ch1}, ch2: {acc_ch2}, ch3: {acc_ch3}'
                print(greeting)
                await websocket.send(greeting)
            else:
                await websocket.send(greeting)
        except websockets.ConnectionClosedError:
            print("客户已断开")
            print(f"已经保存{i}条数据")

            return True

start_server = websockets.serve(startServer, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(asyncio.shield(start_server))
asyncio.get_event_loop().run_forever()
