#!python3

import irsdk
import time
import socket
from pythonping import ping



# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

chairConnected = False
# here we check if we are connected to iracing
# so we can retrieve some data
def check_iracing():
    if state.ir_connected and not (ir.is_initialized and ir.is_connected):
        state.ir_connected = False
        # don't forget to reset your State variables
        state.last_car_setup_tick = -1
        # we are shutting down ir library (clearing all internal variables)
        ir.shutdown()
        print('irsdk disconnected')
    elif not state.ir_connected and ir.startup() and ir.is_initialized and ir.is_connected:
        state.ir_connected = True
        print('irsdk connected')
        
def check_chair():
    ping('192.168.0.11', verbose=True )

# our main loop, where we retrieve data
# and do something useful with it
def loop():

    t = ir['SessionTime']
    print('session time:', t)

    speed = ir['Speed']
    print('Speed:', speed)
    
    if chairConnected:
        sendData()
        print('Data send to chair')


def sendData():
    UDP_IP = "192.168.235.1"
    UDP_PORT = 5005
    MESSAGE = b"Test01 to %s" % UDP_IP
    print("UDP target IP: %s" % UDP_IP)
    print("UDP target port: %s" % UDP_PORT)
    print("message: %s" % MESSAGE)
    sock = socket.socket(socket.AF_INET, # Internet
                          socket.SOCK_DGRAM) # UDP
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))



if __name__ == '__main__':
    # initializing ir and state
    ir = irsdk.IRSDK()
    state = State()

    try:
        # infinite loop
        while True:
            # check if we are connected to iracing
            check_iracing()
            # if we are, then process data
            if state.ir_connected:
                loop()
            # sleep for 1 second
            # maximum you can use is 1/60
            # cause iracing updates data with 60 fps
            time.sleep(1)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
