import _thread
import time

def print_time(name,delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print("{} : {} ".format(name,time.ctime(time.time())))

def run():
    try:
        _thread.start_new_thread(print_time, ("Thread-1", 2,))
        _thread.start_new_thread(print_time, ("Thread-2", 4,))
    except:
        print("Error: 无法启动线程")

    while 1:
        pass

if __name__ == '__main__':
    run()