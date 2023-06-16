import time
import socket
from pythonping import ping


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
    
    sendData(pitchAxis, rollAxis, vertAxis, yawAxis, latAxis, longAxis, 59999)  # default values
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

print("Test started")
move(transformData(0.),transformData(0),transformData(0.),transformData(0),transformData(0),transformData(0))