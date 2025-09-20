import vpython as vp
import math

K = 9e9 # Nm^2/C

class Electron:
    def __init__(self):
        self.velocity = vp.vec(0.1,0,0) # m/s
        self.charge = 1.6e-19 # C
        self.mass = 9.1e-31 # kg
        self.object = vp.sphere(
                pos=vp.vec(0,0,0), # m
                radius=0.1, # just for illustrative purposes
                color=vp.color.yellow)

    def tick(self, tickspeed, charged_objects):
        # find force
        electric_potential = calculate_electric_potential(pos=self.object.pos, charged_objects=charged_objects)
        # update position
        self.object.pos += self.velocity * tickspeed



class Electrode:
    def __init__(self, pos, voltage):
        self.object = vp.box(
                pos=pos,
                length=0.5,
                height=2,
                width=2)
        self.voltage = voltage # V


def calculate_electric_potential(pos, charged_objects):
    # args:     pos (vp.vec)
    #           charged_objects (list of objects with either charge or voltage)
    # returns:  electric potential (numeric)
    voltage = 0;
    for object in charged_objects:
        if hasattr(object, 'voltage'):
            voltage += object.voltage
        elif hasattr(object, 'charge'):
            # get distance
            distance = find_distance(pos, object.object.pos)
            voltage += (K * object.charge) / distance

    return voltage

def calculate_electric_field(pos, charged_objects):
    # args:     pos1, pos2 (vp.vec)
    #           voltage1, voltage2 (numeric)
    # returns:  electric field (vp.vec)
    # this is kinda inefficient and probably buggy, but idk how to do this better and still be general
    # find x component
    # find y component
    # find z component
    # find direction of gradient
    # 

    return 
        

def find_distance(pos1, pos2):
    distance = math.sqrt(
            (pos1.x - pos2.x) ** 2 +
            (pos1.y - pos2.y) ** 2 +
            (pos1.z - pos2.z) ** 2 
    )
    return distance


def main():
    tickspeed = 0.1
    electron = Electron()
    anode = Electrode(pos=vp.vec(10,0,0), voltage=5)
    cathode = Electrode(pos = vp.vec(0,0,0), voltage=0)
    # main loop
    while True:
        vp.rate(30)
        electron.tick(tickspeed)


main()
