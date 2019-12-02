# -*- coding: UTF-8 -*-
import os
import sys
import serial
import time
import random
import datetime

##打印串口的波特率
#SERIAL_BAUDRATE=115200
#
#
#
#USB开关控制器的波特率
CONTROL_SERIAL_BAUDRATE=9600


def _help():
    print('''
    Usage:
        python3 test_power.py reboot comPortReset

        comPortReset ：USB开关控制器控制开发板复位使用的COM口

    Example:
        python3 test_power.py reboot COM1

    ''')
#ps 4Byte:[default:0x0A][CHANNEL][0x00:on,0x01:off][checksum]
def powerControl(ser, status):
    if status == "off":
        code=bytes.fromhex("a0 01 00 a1")
        ser.write(code)
        code=bytes.fromhex("a0 02 00 a2")
        ser.write(code)
    if status == "on":
        code = bytes.fromhex("a0 01 01 a2")
        ser.write(code)
        code = bytes.fromhex("a0 02 01 a3")
        ser.write(code)


def reboot(comPortReset):
    ser_reset=serial.Serial(comPortReset,CONTROL_SERIAL_BAUDRATE)
    f = open("output_log.txt", "w")     # 打开文件以便写入
    time_stamp = datetime.datetime.now()
    f.write("Start test at %s.\n----------------------------------\n" % (time_stamp.strftime('%Y.%m.%d-%H:%M:%S')))
    f.close()

    reboot_time = 0
    while reboot_time < 100:
        powerControl(ser_reset, "off")      # 需要测试程序在开始延时几秒
        tm = 1 + random.random() / 2        # 1s + 随机数
        time.sleep(tm)
        print("pwr off. sleep ", tm, "sec");

        f = open("output_log.txt", "a")     # 打开文件以便写入
        f.write("pwr off. sleep %0.3f sec.\n" % (tm))

        powerControl(ser_reset, "on")
        tm = 2.5 + random.random()            # 2s + 随机数(0~0.5)
        time.sleep(tm)                      # 开机时间
        reboot_time = reboot_time + 1
        print("pwr on.", reboot_time, ":", tm, "sec");
        f.write("pwr on.        %0.3f sec.\n" % (tm))
        f.close()

    ser_reset.close()

def poweroffon(comPortReset):
    ser_reset=serial.Serial(comPortReset,CONTROL_SERIAL_BAUDRATE)

    powerControl(ser_reset, "off")      # 需要测试程序在开始延时几秒
    tm = 1 + random.random()            # 1s + 随机数
    time.sleep(tm)
    powerControl(ser_reset, "on")

    ser_reset.close()

def poweroff(comPortReset):
    ser_reset=serial.Serial(comPortReset,CONTROL_SERIAL_BAUDRATE)
    powerControl(ser_reset, "off")      # 需要测试程序在开始延时几秒
    ser_reset.close()

def reset(comPortReset):
    ser_reset=serial.Serial(comPortReset,CONTROL_SERIAL_BAUDRATE)

    reboot_time = 0
    while reboot_time < 100:
        powerControl(ser_reset, "on")      # 需要测试程序在开始延时几秒
        tm = 1
        time.sleep(tm)

        powerControl(ser_reset, "off")
        tm = 2.5 + random.random()          # 2s + 随机数(0~0.5)
        time.sleep(tm)                      # 开机时间
        reboot_time = reboot_time + 1
        print("reset", reboot_time, ":", tm, "sec");

    ser_reset.close()


if __name__ == '__main__':
    arg_num = len(sys.argv)
    if arg_num == 5 and sys.argv[1] == "runBoard":
        runImage(sys.argv[2], sys.argv[3], sys.argv[4])
    elif arg_num == 3 and sys.argv[1] == "reboot":
        reboot(sys.argv[2])
    elif arg_num == 3 and sys.argv[1] == "poffon":
        poweroffon(sys.argv[2])
    elif arg_num == 3 and sys.argv[1] == "poff":
        poweroff(sys.argv[2])
    elif arg_num == 3 and sys.argv[1] == "reset":
        reset(sys.argv[2])
    else:
        _help()



