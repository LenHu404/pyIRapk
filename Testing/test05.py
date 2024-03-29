#!python3

import irsdk
import time
import socket
from pythonping import ping

#use to strengthened or weaken each movement
pitchGain = 6
rollGain = 5
yawGain = 0.3
heaveGain = 0.09
latGain = 0.3
longGain = 4

chairConnected = True
DebugMode = False
# this is our State class, with some helpful variables
class State:
    ir_connected = False
    last_car_setup_tick = -1

# here we check if we are connected to iracing
# so we can retrieve data
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

def check_FestoCOntroller():
    ping('192.168.0.11', verbose=True )

# our main loop, where we retrieve data
# and do something useful with it
def loop():

    t = ir['SessionTime']
    print('session time:', t)

                      
    pitch = ir['Pitch'] * pitchGain * -1 # minus 1 bc the chair uses it the other way
    print('Pitch:', pitch)
    
    Roll = ir['Roll'] * rollGain
    print('Roll:', Roll)

    VertAccel = (ir['VertAccel'] - 9.8) * heaveGain # minus 9.8 to compensate for gravity
    print('VertAccel:', VertAccel)

    
    #YawRate = ir['YawRate'] * yawGain  
   #print('YawRate:', YawRate)

    LatAccel = ir['LatAccel'] * latGain
    print('LatAccel:', LatAccel)

    LongAccel= ir['LongAccel'] * longGain
    print('LongAccel:', LongAccel)


    
    
    if chairConnected:
        move(transformData(pitch), transformData(Roll), transformData(VertAccel), transformData(YawRate), transformData(LatAccel), transformData(LongAccel))
        #print('Data send to chair')


def sendData(PitchAxis, RollAxis, HeaveAxis, YawAxis, LateralAxis, LongAxis, port):
    host = "192.168.0.10"  # IP of Festo PC 
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
                                #s is the string with the data in expod formation (d0000:0000:0000:0000:0000:0000e) this can be seen with wireshark
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
    return scaleToBounds(value, 600)
    
  
def clampToOne(value):
    return max(-1.0, min( 1.0, value))

def scaleToBounds(value, multiplier):
    result = value * multiplier
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
    
    if (DebugMode != True):
        #sendData(pitchAxis, rollAxis, vertAxis, yawAxis, latAxis, longAxis, 59999)  # default values
        #sendData(pitchAxis, "0000", "0000", "0000", "0000", "0000", 59999)  # default values
        sendData(pitchAxis, rollAxis, "0000", yawAxis, "0000", "0000", 59999)  #only rotations
        #sendData( "0000",  "0000", vertAxis,  "0000", latAxis, longAxis, 59999)  # only directional forces


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
