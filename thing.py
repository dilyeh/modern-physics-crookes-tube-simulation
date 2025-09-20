import vpython as vp
import math
import random

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
        # get force
        electric_field = find_electric_field(self.object.pos, charged_objects)
        force = self.charge * electric_field
        accel = force / self.mass

        # update position
        self.velocity += accel * tickspeed
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
    cathode = Electrode(pos = vp.vec(0,0,0), charge=0, color=vp.color.blue)

    accelerating_anodes = [
        Electrode(pos=vp.vec(10,0,0), charge=1e-8, color=vp.color.red),
        Electrode(pos=vp.vec(20,-5,0), charge=1e-8, color=vp.color.red),
        #Electrode(pos=vp.vec(20,5,0), charge=1e-8, color=vp.color.red),
    ]

    electrons = [Electron(vp.vec(1,0,0)), Electron(vp.vec(4,1,0))]

    vp.scene.autoscale = False
    vp.scene.camera.pos = vp.vec(5,0,0)
    tickspeed = 5e-8
    tickNum = 0
    # main loop
    while True:
        vp.rate(60)
        tickNum += 1
        # create electrons
        if tickNum > 50:
            tickNum = 0
            electrons.append(Electron(vp.vec(1,0,0)))

        # move all the stuff
        for electron in electrons:
            electron.tick(tickspeed, accelerating_anodes)

        # delete electrons out of range
        for electron in electrons:
            if electron.object.pos.x > 50:
                del electron



main()
