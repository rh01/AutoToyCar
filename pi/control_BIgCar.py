#!/usr/bin/python2
#coding:utf-8
import socket
# from rpiGPIO import *
import RPi.GPIO as GPIO
import time


dc = 30
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

GPIO.output(15, GPIO.HIGH)
GPIO.output(18, GPIO.HIGH)

p1 = GPIO.PWM(15, 50)
p1.start(0)
p1.ChangeDutyCycle(dc)

p2 = GPIO.PWM(18, 50)
p2.start(0)
p2.ChangeDutyCycle(dc)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)


t = 0.03


class rpiGPIOHelper(object):
    # 初始化设置引脚输出
    def init(self):
        print "start recving command data......"


        GPIO.setup(11, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)

        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(16, GPIO.OUT)



        self.reset()

    # 所有引脚置低电平，用于复位、停止运行的功能
    def reset(self):
        GPIO.output(11, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(12, GPIO.LOW)
        GPIO.output(16, GPIO.LOW)



    # back 11->1 13->0 12->1 16->0 反转
    def down(self):
        GPIO.output(11, GPIO.HIGH)
        GPIO.output(13, GPIO.LOW)

        GPIO.output(12, GPIO.HIGH)
        GPIO.output(16, GPIO.LOW)

        time.sleep(t)
        self.reset()
        print "pi car backward"


    # front 11->0 13->1 12->0 16->1 正转
    def up(self):
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)

        time.sleep(t)
        self.reset()
        print "pi car forwarding."

    def turnleft(self):
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)


        GPIO.output(16, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)
        p1.ChangeDutyCycle(10)
        p2.ChangeDutyCycle(30)


        time.sleep(t)
        self.reset()
        print "pi car turnright"

    def turnright(self):
        GPIO.output(13, GPIO.HIGH)
        GPIO.output(11, GPIO.LOW)

        GPIO.output(16, GPIO.HIGH)
        GPIO.output(12, GPIO.LOW)

        p2.ChangeDutyCycle(10)
        p1.ChangeDutyCycle(30)

        time.sleep(t)
        self.reset()
        print "pi car turnleft"

    def clean(self):
        global recv_turn
        GPIO.cleanup()
        recv_turn = False
        print "Clean Done!!!!"


# constructure class object
gpio_helper = rpiGPIOHelper()

# recv_turn

recv_turn = True

# ============socket================ #
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('172.14.1.126', 8004))
# ============socket================ #



while recv_turn:
    pre_data = s.recv(1024)
    print pre_data
    data = pre_data.split('O')[0]
    if not data: continue
    func = getattr(gpio_helper, data)
    func()
    # s.sendall(data + " had recvied!")

s.close()
