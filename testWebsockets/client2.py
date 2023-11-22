import asyncio

import nidaqmx
import websockets

# 向服务器端认证，用户名密码通过才能退出循环
async def auth_system(websocket):
    while True:
        cred_text = input("please enter your username and password: ")
        await websocket.send(cred_text)
        response_str = await websocket.recv()
        print(f"{response_str}")
        if "congratulation" in response_str:
            return True

# 向服务器端发送认证后的消息
async def send_msg(websocket,datalist):
    # while True:
        # _text = input("please enter your context: ")
        # if _text == "exit":
        #     print(f'you have enter "exit", goodbye')
        #     await websocket.close(reason="user exit")
        #     return False
        # await websocket.send(_text)
        # recv_text = await websocket.recv()
        # print(f"{recv_text}")
    print("-------start send data to server!----")
    for data in datalist:
        await websocket.send(str(data))
        print(f"---->have send the data : {data}")
        rec_str = await websocket.recv()
        print(f"***** server say : {rec_str}")

    print("-------send data to server finished!----")


async def getdatalist():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0")

        # print('1 Channel 1 Sample Read: ')
        datalist = task.read(number_of_samples_per_channel=100)
        return datalist
# 客户端主逻辑
async def main_logic():

    async with websockets.connect('ws://localhost:6678') as websocket:

        await auth_system(websocket)

        await send_msg(websocket,await getdatalist())

asyncio.get_event_loop().run_until_complete(main_logic())