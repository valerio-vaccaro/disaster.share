import time
import serial
import math
import base64
import hashlib
import json

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
       port='/dev/cu.SLAB_USBtoUART5',
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

print("start")
serwrite('/join REC')

received_message = {}

while 1:
    out = serread()
    #if out != '':
    #    print("received: " + out)
    if out.find('>') != -1:
        (pre, post) = out.split('>')
        if post.find(':') != -1:
            (sender, hash, packet_num, total_packets_num, payload) = post.split(':')
            if hash not in received_message:
                received_message[hash] = {}
                received_message[hash]['packets'] = {}
                received_message[hash]['sender'] = sender
                received_message[hash]['total_packets'] = total_packets_num
            received_message[hash]['packets'][packet_num] = payload
            missing_pkts = ''
            delete_messages = []
            for message in received_message:
                missing = False
                message_buf = ''
                for i in range(1, int(received_message[message]['total_packets'], 16) + 1):
                    index = hex(i)[2:]
                    if index not in received_message[message]['packets']:
                        missing_pkts = '{} {}'.format(missing_pkts, index)
                        missing = True
                    else:
                        message_buf = message_buf + received_message[message]['packets'][hex(i)[2:]]
                if not missing:
                    big_tx = base64.a85decode(message_buf.encode('ascii')).decode('ascii')
                    hash = hashlib.sha256(big_tx.encode('ascii')).hexdigest()[:8]
                    if message == hash:
                        print('Receive message {} from {} in {} packets with payload {}'.format(message, sender, int(received_message[message]['total_packets'], 16), big_tx))
                        delete_messages.append(hash)
                    else:
                        print('Receive message {} from {} in {} packets but hash is wrong'.format(message, sender, int(received_message[message]['total_packets'], 16)))
                else:
                    print('Receive message {} from {} in {} packets. Waiting for:{}'.format(message, sender, int(received_message[message]['total_packets'], 16), missing_pkts))

            for delhash in delete_messages:
                del received_message[delhash]

ser.close()
