# -*- coding: utf-8 -*-
import serial

hexString = lambda byteString: " ".join(x.encode('hex') for x in byteString)

#bad but working
import sys
try:
    sys.path.insert(0, 'd:\\Azat\\PycharmProjects\\first')
    from crc16 import checkCRC, addCRC
    #from ttcpServer import simpleCheck
except:
    print "Smth is wrong in import"

ser = serial.Serial()
# set up serial settings
ser.baudrate = 19200
ser.port = 'COM5'
ser.bytesize = 8
ser.parity = 'E'
ser.stopbits = 1
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 0.5

print "Serial settings:", ser
ser.open()

def one_shot(q):
    q = addCRC(q)
    ser.write(q)
    a = ser.read(size=1024)
    print hexString(a)

import struct
def send_modbus_request(req=[1, 3, 40960, 105]):
    req[2] -= 1
    req_str = struct.pack(">bbHH", *req)
    req_str = addCRC(req_str)
    one_shot(str(req_str))

#first 10 regs
one_shot('\x02\x04\x00\x00\x00\x0a')
send_modbus_request([2, 4, 1, 10])


send_modbus_request([2, 6, 13, 255])
send_modbus_request([2, 6, 14, 0])

send_modbus_request([2, 6, 15, 5])
send_modbus_request([2, 6, 16, 4])
send_modbus_request([2, 6, 17, 1])
send_modbus_request([2, 6, 18, 2])
send_modbus_request([2, 6, 19, 3])

send_modbus_request([2, 6, 20, 9])
send_modbus_request([2, 6, 21, 19])
send_modbus_request([2, 6, 22, 39])
send_modbus_request([2, 6, 23, 59])
send_modbus_request([2, 6, 24, 79])

#start leds
one_shot('\x02\x05\x00\x00\xff\x00')
one_shot('\x02\x05\x00\x01\x00\x00')
one_shot('\x02\x05\x00\x02\x00\x00')
one_shot('\x02\x05\x00\x03\x00\x00')
one_shot('\x02\x05\x00\x04\x00\x00')

for i in range(0,89,1):
    send_modbus_request([2, 6, 20, i])
exit()
#set up
one_shot('\x02\x06\x00\x0c\x00\xff')    #4x0013
one_shot('\x02\x06\x00\x0d\x00\x00')    #4x0014
#led 1
one_shot('\x02\x06\x00\x0e\x00\x05')    #4x0015
one_shot('\x02\x06\x00\x13\x00\x23')    #4x0020
#led 2
one_shot('\x02\x06\x00\x0f\x00\x04')    #16
one_shot('\x02\x06\x00\x14\x00\x4B')    #21
#led 3
one_shot('\x02\x06\x00\x10\x00\x01')    #17
one_shot('\x02\x06\x00\x15\x00\x0a')    #22
#led 4
one_shot('\x02\x06\x00\x11\x00\x02')    #18
one_shot('\x02\x06\x00\x16\x00\x55')    #23
#led 5
one_shot('\x02\x06\x00\x12\x00\x03')    #19
one_shot('\x02\x06\x00\x17\x00\x32')    #24
