import math

def show(coords):
    for line in coords:
        print(line)

def center(coords):
    xVal, yVal, zVal = float(coords[0][0]), float(coords[0][1]), float(coords[0][2])
    for i in range(6):
        for j in range(3):
            if(j==0):
                coords[i][j] = float(coords[i][j]) - xVal
            elif(j==1):
                coords[i][j] = float(coords[i][j]) - yVal
            else:
                coords[i][j] = float(coords[i][j]) - zVal
    return coords

def rotY(coords):
    angle = math.atan(coords[1][1]/coords[1][0])
    for i in range(6):
        coords[i][0], coords[i][1], coords[i][2] = coords[i][0]*math.cos(angle) + coords[i][1] * math.sin(angle), -(coords[i][0]*math.sin(angle)) + coords[i][1]*math.cos(angle), coords[i][2]
    return coords

def rotZ(coords):
    angle = math.atan(coords[1][2]/coords[1][0])
    for i in range(6):
        coords[i][0], coords[i][1], coords[i][2] = coords[i][0]*math.cos(angle)+coords[i][2]*math.sin(angle), coords[i][1], -(coords[i][0]*math.sin(angle))+coords[i][2]*math.cos(angle)
    return coords

def planar(coords):
    angle = math.atan(coords[2][2]/coords[2][1])
    for i in range(6):
        coords[i][0], coords[i][1], coords[i][2] = coords[i][0], coords[i][1]*math.cos(angle) + coords[i][2]*math.sin(angle), -(coords[i][1]*math.sin(angle))+coords[i][2]*math.cos(angle)
    return coords

def align(coords):
    coords = center(coords)
    coords = rotY(coords)
    coords = rotZ(coords)
    coords = planar(coords)
    return coords
