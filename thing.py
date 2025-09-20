import vpython as vp
import math

K = 9e9 # Nm^2/C

class Electron:
    def __init__(self, pos):
        self.velocity = vp.vec(0.1,0,0) # m/s
        self.charge = 1.6e-19 # C
        self.mass = 9.1e-31 # kg
        self.object = vp.sphere(
                pos=pos, # m
                radius=0.1, # just for illustrative purposes
                color=vp.color.yellow)

    def tick(self, tickspeed, charged_objects):
        # update position
        self.object.pos += self.velocity * tickspeed



class Electrode:
    def __init__(self, pos, charge, color=vp.vec(0.8,0.8,0.8)):
        self.object = vp.box(
                pos=pos,
                length=0.5,
                height=2,
                width=2,
                color=color)
        self.charge = charge # C

def find_distance(pos1, pos2):
    distance = math.sqrt(
            (pos1.x - pos2.x) ** 2 +
            (pos1.y - pos2.y) ** 2 +
            (pos1.z - pos2.z) ** 2 
    )
    return distance

def find_electric_field(pos, charged_objects):
    electric_field = vp.vec(0,0,0)
    for object in charged_objects:
        distance = find_distance(pos, object.object.pos)
        mag = (K * object.charge) / (distance ** 2)
        # oh nooooo turn magnitude into 3 dimensional components NOOOOOOOOOOOO
        # oh wait just scale the vector lol
        vec_to_obj = object.object.pos - pos
        
        ratio = mag / distance
        indv_field = vec_to_obj * ratio
        electric_field += indv_field

    return electric_field


def main():
    tickspeed = 0.1
    electron = Electron(vp.vec(1,0,0))
    anode = Electrode(pos=vp.vec(10,0,0), charge=1e-8, color=vp.color.red)
    cathode = Electrode(pos = vp.vec(0,0,0), charge=0, color=vp.color.blue)

    electron2 = Electron(vp.vec(4,1,0))
    
    anode_ef = find_electric_field(electron.object.pos, [anode, cathode])
    anode_ef2 = find_electric_field(electron2.object.pos, [anode, cathode])
    print(anode_ef)

    test1 = vp.arrow(pos=electron.object.pos, axis=anode_ef, opacity=0.5, shaftwidth=0.1)
    test2 = vp.arrow(pos=electron2.object.pos, axis=anode_ef2, opacity=0.5, shaftwidth=0.1)



main()
