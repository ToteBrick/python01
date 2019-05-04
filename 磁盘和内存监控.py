# 磁盘使用率
import psutil
import time

disk = psutil.disk_partitions()
for i in disk:
    print("磁盘：%s   分区格式:%s" % (i.device, i.fstype))
    disk_use = psutil.disk_usage(i.device)

    print("使用了：%.1fGB,空闲：%.1fGB,总共：%.1fGB,使用率\033[1;31;42m%s%%\033[0m," % (
        disk_use.used / 1024 / 1024 / 1024, disk_use.free / 1024 / 1024 / 1024, disk_use.total / 1024 / 1024 / 1024,
        disk_use.percent))

time.sleep(1)
cpu_used = psutil.cpu_percent()

print("当前cpu利用率：\033[1;31;42m%s%%\033[0m" % cpu_used)

# 2．  监控服务器内存使用率

memory = psutil.virtual_memory()
# memory.used  使用的
# memory.total  总共
ab = float(memory.used) / float(memory.total) * 100
print("%.2f%%" % ab)

print(psutil.swap_memory())
