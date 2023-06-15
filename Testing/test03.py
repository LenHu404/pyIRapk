def toHexapodString(_f):
    res = "1" if _f < 0 else "0"
    res += str(abs(_f)).zfill(3)
    return res

print("Test", toHexapodString(-23.12))