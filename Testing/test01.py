#!python3

import irsdk
import time
import socket
from pythonping import ping



# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

chairConnected = True
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
        
def check_ControlPC():
    ping('192.168.0.10', verbose=True )

# our main loop, where we retrieve data
# and do something useful with it
def loop():

    t = ir['SessionTime']
    print('session time:', t)

    #speed = ir['Speed']
    #print('Speed:', speed)

                      
    pitch = ir['Pitch']
    print('Pitch:', pitch)
    
    Roll = ir['Roll']
    print('Roll:', Roll)

    VertAccel = ir['VertAccel'] # 9.806662559509277
    print('VertAccel:', VertAccel)

    Yaw = ir['Yaw']
    print('Yaw:', Yaw)

    LatAccel = ir['LatAccel']
    print('LatAccel:', LatAccel)

    LongAccel= ir['LongAccel']
    print('LongAccel:', LongAccel)


    #PitchRate = ir['PitchRate'] #8.786555127926476e-08
    #print('PitchRate:', PitchRate)
    #PitchRate_ST = ir['PitchRate_ST'] #[3.257972593928571e-07, 3.3143493283205316e-07, 3.4653390912353643e-07, 2.409470312159101e-07, 1.5829981236947788e-07, 8.786555127926476e-08]
    #print('PitchRate_ST:', PitchRate_ST)

    
    #RollRate = ir['RollRate'] #3.12117554130964e-05
    #print('RollRate:', RollRate)
    #RollRate_ST = ir['RollRate_ST'] #[-3.5479733924148604e-05, -3.106678923359141e-05, -2.1410816771094687e-05, -6.255076186789665e-06, 1.1896221622009762e-05, 3.12117554130964e-05]
    #print('RollRate_ST:', RollRate_ST)

    #VertAccel = ir['VertAccel'] # 9.806662559509277
    #print('VertAccel:', VertAccel)

    #VertAccel_ST = ir['VertAccel_ST'] # [9.806638717651367, 9.806638717651367, 9.806644439697266, 9.806645393371582, 9.806645393371582, 9.806646347045898]
    #print('VertAccel_ST:', VertAccel_ST)

    
    
    if chairConnected:
        move(transformData(pitch), transformData(Roll), VertAccel, transformData(Yaw), LatAccel, LongAccel)
        #print('Data send to chair')


#def sendData():
#    UDP_IP = "192.168.235.1"
#    UDP_PORT = 5005
#    MESSAGE = b"Test01 to %s" % UDP_IP
#    print("UDP target IP: %s" % UDP_IP)
#    print("UDP target port: %s" % UDP_PORT)
#    print("message: %s" % MESSAGE)
#    sock = socket.socket(socket.AF_INET, # Internet
#                          socket.SOCK_DGRAM) # UDP
#    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

def sendData(PitchAxis, RollAxis, HeaveAxis, YawAxis, LateralAxis, LongAxis, port):
    host = "192.168.0.10"  # Replace with your desired IP address
    endpoint = (host, port)
    udpClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    str = ":"
    Faultys = ""

    if len(PitchAxis) == 4:
        if len(RollAxis) == 4:
            if len(HeaveAxis) == 4:
                if len(YawAxis) == 4:
                    if len(LateralAxis) == 4:
                        if len(LongAxis) == 4:
                            try:
                                s = "d" + PitchAxis + str + RollAxis + str + HeaveAxis + str + YawAxis + str + LateralAxis + str + LongAxis + "e"
                                if s != "":
                                    bytes = s.encode('utf-8')  
                                    udpClient.sendto(bytes, endpoint)
                                #elif len(IncommingNews) > 0:
                                    #bytes = str(IncommingNews[0]).encode('utf-8')
                                    #udpClient.sendto(bytes, endpoint)
                            except Exception as ex:
                                Faultys.append(ex)
                        else:
                            Faultys.append("Longaxis.text is too long or too short")
                    else:
                        Faultys.append("Lateralaxis.text is too long or too short")
                else:
                    Faultys.append("Yawaxis.text is too long or too short")
            else:
                Faultys.append("Heaveaxis.text is too long or too short")
        else:
            Faultys.append("Rollaxis.text is too long or too short")
    else:
        Faultys.append("Pitchaxis.text is too long or too short")

    # transorming Data to fit the scale of Data the chair can use
def transformData(_value):
    value = clampToOne(_value)
    return scaleToBounds(value, -600, 600)
    
  
def clampToOne(value):
    return max(-1.0, min( 1.0, value))

def scaleToBounds(value, min, max):
    result = value *( min if value > 0 else max)
    return result

def move(_pitchAxis, _rollAxis, _vertAxis, _yawAxis, _latAxis, _longAxis):
    # convert vectors to string-components and send to X6
    pitchAxis = toHexapodString(_pitchAxis)
    rollAxis = toHexapodString(_rollAxis)
    vertAxis = toHexapodString(_vertAxis)
    yawAxis = toHexapodString(_yawAxis)
    latAxis = toHexapodString(_latAxis)
    longAxis = toHexapodString(_longAxis)
    # X6.SendData(xRot, zRot, yPos, yRot, xPos, zPos, 59999)  # default values
    # X6.SendData(zPos, zRot, yPos, xPos, yRot, xRot, 59999)  # switched values
    # X6.SendData(xRot, zRot, yRot, yPos, xPos, zPos, 59999)  # default values
    
    #sendData(pitchAxis, rollAxis, vertAxis, yawAxis, latAxis, longAxis, 59999)  # default values
    print('Data send to chair')

    # X6.SendData("0", "0", "0", xPos, yPos, zPos, 59999)  # default values
    #print("Pos: " + str(_position) + ", rot" + str(_rotation))
    print('pitchAxis:', pitchAxis)
    print('rollAxis:', rollAxis)
    print('vertAxis:', vertAxis)
    print('yawAxis:', yawAxis)
    print('latAxis:', latAxis)
    print('longAxis:', longAxis)
    # Debug.Log("zPos: "+zPos + ", zRot: " + zRot + ",yPos: " + yPos + ",xPos" + xPos + ",yRot: " + yRot + ",xRot: " + xRot)

# create a three-digit string with leading 1 (-) or 0 (+) according to the sign
def toHexapodString(_f):
    res = "1" if _f < 0 else "0"
    res += str(int(abs(_f))).zfill(3)
    return res

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
            time.sleep(1/60)
    except KeyboardInterrupt:
        # press ctrl+c to exit
        pass
