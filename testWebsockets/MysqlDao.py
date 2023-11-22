from mysql import connector


def Myconn(user,password,host,databasename):
    conn=None
    try:
        conn = connector.connect(
            user=user,
            password=password,
            host=host,
            database=databasename
        )
    except Exception:
        print("connect error")
        exit(1)
    else:
        return conn

def selectAll(con,TBname):
    cursor=con.cursor()
    query="select * from {}".format(TBname)
    try:
        cursor.execute(query)
    except Exception:
        print("查询出错！")
        exit(1)
    else:
        return cursor

def insert2(conn,data1,data2):
    sql = "INSERT into nitest(`ai0`,`ai1`) VALUES({},{})".format(data1,data2)
    cursor=conn.cursor()
    try:
        cursor.execute(sql)

    except Exception:
        print("插入出错！")
        exit(1)
    else:
        return cursor

    def insert(conn, colnum, data):
        sql = "INSERT into nitest(`ai{}`) VALUES({})".format(colnum, data)
        cursor = conn.cursor()
        try:
            cursor.execute(sql)

        except Exception:
            print("插入出错！")
            exit(1)
        else:
            return cursor
# if __name__ == '__main__':
#         conn = Myconn("root", "123456", "127.0.0.1", "test")
#         insert2(conn,"111","312312")
#         print(conn)
#         conn.commit()
#         conn.close()