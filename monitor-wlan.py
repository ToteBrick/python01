from tkinter import *
import psutil
import time
import threading


def net_state():
    # psutil.net_io_counters 网络使用
    # while True:
    # 无线网卡接收数据
    recv1 = psutil.net_io_counters(pernic=True)['WLAN'][1]
    send1 = psutil.net_io_counters(pernic=True)['WLAN'][0]
    time.sleep(1)  # 每隔1s监听端口接收数据
    recv2 = psutil.net_io_counters(pernic=True)['WLAN'][1]
    send2 = psutil.net_io_counters(pernic=True)['WLAN'][0]
    # 上传数据
    return 'upload:%.1f kb/s.' % ((send2 - send1) / 1024.0), 'download:%.1f kb/s.' % ((recv2 - recv1) / 1024.0)


while True:
    s1 = net_state()[0]
    s2 = net_state()[1]
    print('当前上传和下载速度为:')
    print(s1)
    print(s2)
    print('---------------------')

