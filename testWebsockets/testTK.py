import random
import time
from tkinter import *
import nidaqmx
import pymysql
from threading import Thread  # 创建线程的模块

# 开关
qq = 1

#NI采集程序
def qwer():
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1")
        task.timing.cfg_samp_clk_timing(
            rate=10000,
            sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
            samps_per_chan=100000
        )
        datalist = task.read()
    return datalist

#采集数据并插入数据库
def insert():
    global qq
    if qq == 2:
        qq =1

    # 连接数据库
    conn = pymysql.connect(host='127.0.0.1'  # 连接名称，默认127.0.0.1
                           , user='root'  # 用户名
                           , passwd='123456'  # 密码
                           , port=3306  # 端口，默认为3306
                           , db='test'  # 数据库名称
                           , charset='utf8'  # 字符编码
                           , database='nidata'
                           )
    try:
        conn.ping()
        txt.insert(END, "数据库已连接...\n")
    except:
        txt.insert(END, "数据库连接异常，请重试\n")
        return
    cur = conn.cursor()  # 生成游标对象
    txt.insert(END, "START...\n")
    while qq < 2:
        datalist = qwer()
        sql = "INSERT into test(`data0`,`data1`)  VALUES({},{})".format(datalist[0], datalist[1])  # SQL语句
        cur.execute(sql)  # 执行SQL语句
        txt.insert(END, datalist)  # 追加显示运算结果
        txt.insert(END, "\n")
        root.update()
        # print(datalist)
        # time.sleep(1)
    root.update()
    txt.insert(END, "END...\n")
    conn.commit()
    cur.close()
    conn.close()
    txt.insert(END, "数据库已断开...\n")
    # print("END...")


# def startInsert():
#     # 开启线程  参数1：方法名(不要带括号)   参数2：参数（元祖）      返回对象
#     th = Thread(target=insert(), args='线程1')
#     th.start()  # 只是给操作系统发送了一个就绪信号，并不是执行。操作系统接收信号后安排cpu运行

# 停止采集
def shutInsert():
    global qq
    qq = 2
    root.update()


root = Tk()

root.geometry('460x240')
root.title('数据采集程序')
lb1 = Label(root, text='数据存储到数据库：nidata 表：test',bg='#d3fbfb',font=('华文新魏',20),width=20,height=2,relief=SUNKEN)


lb1.place(relx=0, rely=0, relwidth=1, relheight=0.2)



btn1 = Button(root, text='开始', command=insert)
btn1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)


btn2 = Button(root, text='停止', command=shutInsert)
btn2.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = Text(root)
txt.place(rely=0.3, relheight=0.7)

scroll = Scrollbar()
# 放到窗口的右侧, 填充Y竖直方向
scroll.pack(side=RIGHT, fill=Y)

# 两个控件关联
scroll.config(command=txt.yview)
txt.config(yscrollcommand=scroll.set)

root.mainloop()
