# ----------- server 端 -----------
import asyncio
import websockets

# from testWebsockets import MysqlDao


async def startServer(websocket, path):
    print('-------- server start ------')
    # conn = MysqlDao.Myconn("root", "123456", "127.0.0.1", "test")
    i = 0
    # if conn:
    #     print("------数据库已连接-------")
    while True:
        try:
            rec_data = await websocket.recv()
            # split_data = rec_data.split("|")
            # print(rec_data)
            # MysqlDao.insert(conn,split_data[0],split_data[1])
            split_data = rec_data.split("|")
            print(rec_data)

            # MysqlDao.insert2(conn, split_data[0], split_data[1])
            i += 1
            # if not i%50:
            #     conn.commit()

            greeting = 'server get %s' % rec_data
            await websocket.send(greeting)
        except websockets.ConnectionClosedError:
            print("客户已断开")
            print(f"已经保存{i}条数据")
            # conn.commit()
            # conn.close()
            return True


start_server = websockets.serve(startServer, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(asyncio.shield(start_server))
asyncio.get_event_loop().run_forever()