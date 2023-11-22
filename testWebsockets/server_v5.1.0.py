# ----------- server 端 -----------
# 单通道的降采样1/10
import asyncio
import websockets

async def startServer(websocket, path):
    print('-------- server start ------')
    i = 0
    while True:
        try:
            rec_data = await websocket.recv()
            split_data = rec_data.split("|")
            i += 1

            # 处理第一个通道的数据
            volt_ch1 = float(split_data[0])
            acc_ch1 = volt_ch1 / 101.6

            greeting = "i=" + str(i) + "server recviced,not be used"

            # 降采样,每10个数据点选取一个
            if i % 10 == 0:
                greeting = 'server get ch1: %s' % acc_ch1
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
