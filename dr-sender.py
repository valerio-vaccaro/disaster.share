import time
import serial
import math
import base64
import hashlib

MAX_SIZE = 200
MAGIC = b'BTC'

def serwrite(buff):
    for i in range(0, len(buff)):
        ser.write(buff[i].encode('ascii'))
        time.sleep(0.001)
    ser.write('\r'.encode('ascii'))
    ser.write('\n'.encode('ascii'))

def serread():
    out = ''
    while 1:
        buf = ser.read(1000).decode('ascii')
        time.sleep(0.1)
        if len(buf) == 0:
          break
        out += buf
    return out

ser = serial.Serial(
       port='/dev/cu.SLAB_USBtoUART',
       baudrate=115200,
       timeout=0.1,
       parity=serial.PARITY_NONE,
       stopbits=serial.STOPBITS_ONE,
       bytesize=serial.EIGHTBITS,
       xonxoff = False,     #disable software flow control
       rtscts = False,     #disable hardware (RTS/CTS) flow control
       dsrdtr = False,       #disable hardware (DSR/DTR) flow control
       writeTimeout = 2,     #timeout for writ
)

ser.isOpen()

out = serread()
if out != '':
    print(">>" + out)

serwrite('/join BTC')

out = serread()
if out != '':
    print(">>" + out)


big_tx_b = b'+'+b'12345678'*200+b'+'
big_tx = base64.a85encode(big_tx_b)
packet_num = math.ceil(len(big_tx)/MAX_SIZE)
hash = hashlib.sha256(big_tx_b).hexdigest()[:8]

for i in range(0, packet_num):
    packet = '{}:{}:{}:{}:{}'.format(MAGIC.decode('ascii'), hash, hex(i+1)[2:], hex(packet_num)[2:], big_tx[i*MAX_SIZE:(i+1)*MAX_SIZE].decode('ascii'))
    serwrite(packet)
    time.sleep(2)

    out = serread()
    if out != '':
        print(">>" + out)

ser.close()
