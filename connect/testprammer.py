# f = open("./foo.txt", "w")
# f.write( "Python 是一个非常好的语言。\n是的，的确非常好!!\n" )
# value = f.tell()
# print(value)
#
# f.close()

# f1 = open("/foo.txt", "r")
# data = f1.read()
# print(f1)
# f1.close()
import pickle

# data1 = {'a': [1, 2.0, 3, 4+6j],
#          'b': ('string', u'Unicode string'),
#          'c': None}
#
# selfref_list = [1, 2, 3]
# selfref_list.append(selfref_list)
#
# output = open('data.pkl', 'wb')
#
# # Pickle dictionary using protocol 0.
# pickle.dump(data1, output)
#
# # Pickle the list using the highest protocol available.
# pickle.dump(selfref_list, output, -1)
#
# output.close()
import pprint

# pkl_file = open('data.pkl','rb')
# data = pickle.load(pkl_file)
# pprint.pprint(data)
# data = pickle.load(pkl_file)
# pprint.pprint(data)
# from datetime import date
#
# birthday = date(1998, 3, 4)
# age = date.today() - birthday
# print(age.days)
from datetime import time

import nidaqmx
from mysql import connector

from mysql.connector import errorcode

def Myconn(user,password,host,databasename):
    conn=None;
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

def insert(conn,data):
    sql = "INSERT into nitest(`value`) VALUES(%f)"
    cursor=conn.cursor()
    try:
        cursor.executemany(sql,data)

    except Exception:
        print("查询出错！")
        exit(1)
    else:
        return cursor

def run():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan('Dev1/ai0')
        task.timing.cfg_samp_clk_timing(
            rate=5000,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=40000
        )
        task.start()

        data = task.read(20)
        task.stop()
        print("-------data show------------")
        print(data)
        print("-----------------------------")



    #------------------------------------------
    con = Myconn("root", "123456", "127.0.0.1", "test")
    cursor = con.cursor()
    for da in data:

        sql = "INSERT into nitest(`value`) VALUES({})".format(da)
        cursor.execute(sql)

    con.commit()
    print("sucess!")



def main():

    data = [1.23,4.2323]
    con=Myconn("root","123456","127.0.0.1","test")
    # cursor=selectAll(con,"user")
    cursor = insert(con,data)
    # print("id \t name\t password\t address\t phone\n")
    # for(id,name,password,address,phone)in cursor:
    #     print(id,"\t",name,"\t",password,"\t",address,"\t",phone,"\t\n")
    con.commit()
    cursor.close()
    con.close()


if __name__ == '__main__':
    run()

