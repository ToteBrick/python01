from tkinter import *
import psutil
import time
import sys
sys.setrecursionlimit(2000)


def net_state():
    # psutil.net_io_counters 所有网络使用情况
    # 无线网卡接收数据
    # net_state()
    recv1 = psutil.net_io_counters(pernic=True)['WLAN'][1]
    time.sleep(1)  # 每隔1s监听端口接收数据
    recv2 = psutil.net_io_counters(pernic=True)['WLAN'][1]
    return 'download:%.1f kb/s.' % ((recv2 - recv1) / 1024.0)

    # print('download:%.1f kb/s.' % ((recv2 - recv1) / 1024.0))

# while True:
#     print(net_state())

if __name__ == '__main__':

    root = Tk()
    root.wm_title('WLAN网口:')
    wl = Label(root, text=net_state(), font=("黑体", 20, "bold"), background="black",
               width=20, height=3, foreground='white')
    wl.pack()
    root.mainloop()
