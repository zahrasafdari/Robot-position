
#the coordinates of robot in the space and limits
coordinates = [
    "lx",     #lower limit of x
    "ly",     #lower limit of y
    "ux",     #upper limit of x
    "uy",     #upper limit of y
    "uz",     #upper limit of z
    "lz",     #lower limit of z
    "ox",     #start coordinate of x
    "oy",     #start coordinate of y
    "oz",     #start coordinate of z
]
class Nonefunc:
    pass
Nonefunc = Nonefunc()

#the statements that we use them to move robot in space
statements = {
            "begin": Nonefunc,"east": 1,"west": -1,"north": 1,
            "south": -1,"up": 1,"down": -1,"end": Nonefunc,
}