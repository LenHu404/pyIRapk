def toHexapodString(_f):
    res = "1" if _f < 0 else "0"
    res += str(int(abs(_f))).zfill(3)
    return res

def transformData(_value):
    value = clampToOne(_value)
    return scaleToBounds(value, 600)
    
  
def clampToOne(value):
    return max(-1.0, min( 1.0, value))

def scaleToBounds(value, min, max):
    result = value *( min if value > 0 else max)
    return result

def scaleToBounds2(value, multiplier):
    result = value * multiplier
    return result

value1 = -0.24241
value2 = clampToOne(value1)
value3 = scaleToBounds2(value2,600)
value4 = toHexapodString(value3)

print("value1", value1)
print("value2", value2)
print("value3", value3)
print("value4", value4)