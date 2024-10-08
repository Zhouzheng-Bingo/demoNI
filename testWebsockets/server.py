import asyncio
from asyncio import shield
from asyncio.exceptions import CancelledError

import websockets

# 检测客户端权限，用户名密码通过才能退出循环
async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        print(f" recive the connect require: {recv_str}")

        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)

# 接收客户端消息并处理，这里只是简单把客户端发来的返回回去
async def recv_msg(websocket):
    while True:
        recv_text = await websocket.recv()
        response_text = f"your submit context: {recv_text}"
        print(f"---->receive : {recv_text}")
        await websocket.send("I have recive your message: "+response_text)

# 服务器端主逻辑
# websocket和path是该函数被回调时自动传过来的，不需要自己传
async def main_logic(websocket, path):

        await check_permit(websocket)

        await recv_msg(websocket)



# 把ip换成自己本地的ip
start_server = websockets.serve(main_logic,'localhost', 6678)


# asyncio.get_event_loop().run_until_complete( asyncio.shield(start_server))
asyncio.get_event_loop().run_until_complete(start_server)
print(start_server)
asyncio.get_event_loop().run_forever()