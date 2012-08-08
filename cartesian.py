import align

def intake(geometry):
    file = open(geometry, "r")
    text = file.read()
    file.close()
    words = text.split()
    coords = []
    for i in range(6):
        coords.append([])
        for j in range(3):
            coords[i].append(float(words[i*4+j+1]))
    return align.align(coords)
