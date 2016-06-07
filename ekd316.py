# -*- coding: utf-8 -*-

import serial

hexString = lambda byteString : " ".join(x.encode('hex') for x in byteString)


address = 5
request_input = (
    {"pdu": 2534, "data": ("u22_SuperheatRef", "u21_Superheat", "u20_S2_Temp")        },
    {"pdu": 2541, "data": ("u24_Opening_OD%", "u25_EvapPres_Pe", "u26_EvapTemp_Te", "u27_S3_Temp")   },
)

from spiderSettings import form_modbus_request
request = []
t_name = ()
for r in request_input:
    r_str = form_modbus_request(req=(address, 3, r["pdu"], len(r["data"])))
    request.append(r_str)
    print hexString(r_str)
    t_name += r["data"]

ser = serial.Serial(port="COM3",
                    baudrate=19200,
                    stopbits=1,
                    parity="E",
                    bytesize=8,
                    timeout=0.1)
import struct
from ttcpServer import simpleCheck, rearrangeData
t_div = (10,10,10,1,10,10,10)
unpack_str = (">hhh", ">hhhh")
from datetime import datetime
while 1:
    t_val = ()
    for r,s in zip(request,unpack_str):
        ser.write(r)
        response = ser.read(1024)
        d = simpleCheck(r, response)
        #print hexString(d)
        if d==1:
            print "error in check"
        val_tuple = struct.unpack(s, d)
        t_val += val_tuple
    print datetime.now()," ".join("{}={}".format(n,v/(d*1.0)) for n,v,d in zip(t_name, t_val, t_div))



ser.close()