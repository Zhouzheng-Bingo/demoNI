# ----------- server 端 -----------
# 三个通道降采样，存入opcua节点
import asyncio
import websockets
from opcua import Client

def process_channel_data(channel_data, sensitivity):
    volt = float(channel_data)
    acc = volt / sensitivity
    return acc

def send_data_to_OPC_UA(acc_ch1, acc_ch2, acc_ch3):
    url = "opc.tcp://DESKTOP-VCSTSR6:48020/" # Change to your OPC UA server's URL
    client = Client(url, timeout=600)
    try:
        client.connect()

        var_ch1 = client.get_node("ns=2;i=39")
        var_ch2 = client.get_node("ns=2;i=40")
        var_ch3 = client.get_node("ns=2;i=41")

        var_ch1.set_value(acc_ch1)
        var_ch2.set_value(acc_ch2)
        var_ch3.set_value(acc_ch3)
    finally:
        client.disconnect()

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

            # Send data to OPC UA server
            send_data_to_OPC_UA(acc_ch1, acc_ch2, acc_ch3)

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
