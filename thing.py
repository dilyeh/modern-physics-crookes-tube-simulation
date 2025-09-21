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
                radius=0.2, # just for illustrative purposes
                color=vp.color.yellow)

    def tick(self, tickspeed, charged_objects):
        # get force
        electric_field = find_electric_field(self.object.pos, charged_objects)
        force = self.charge * electric_field
        accel = force / self.mass

        # update position
        self.velocity += accel * tickspeed
        self.object.pos += self.velocity * tickspeed

        if self.object.pos.x > 20:
            del self



class Electrode:
    def __init__(self, pos, charge, size, orientation, color=vp.vec(0.8,0.8,0.8)):
        display_size = vp.vec(0,0,0)
        if orientation == 'x':
            display_size = vp.vec(0.5, size[0], size[1])
        elif orientation == 'y':
            display_size = vp.vec(size[0], 0.5, size[1])
        elif orientation == 'z':
            display_size = vp.vec(size[0], size[1], 0.5)

        self.object = vp.box(
                pos=pos,
                length=display_size.x,
                height=display_size.y,
                width=display_size.z,
                color=color,
                opacity=0.5)
        self.size = size
        self.orientation = orientation
        self.charge = charge # C


def find_distance(pos1, pos2):
    distance = math.sqrt(
            (pos1.x - pos2.x) ** 2 +
            (pos1.y - pos2.y) ** 2 +
            (pos1.z - pos2.z) ** 2 
    )
    return distance


def find_closest_point(pos, electrode):
    # basically finds the point on a 2d surface closest to a given point in 3d
    point = (0,0)
    surface_center = (0,0)
    size = electrode.size

    # collapse into a 2d plane
    if electrode.orientation == 'x':
        point = (pos.y, pos.z)
        surface_center = (electrode.object.pos.y, electrode.object.pos.z)
    elif electrode.orientation == 'y':
        point = (pos.x, pos.z)
        surface_center = (electrode.object.pos.x, electrode.object.pos.z)
    elif electrode.orientation == 'z':
        point = (pos.x, pos.y)
        surface_center = (electrode.object.pos.x, electrode.object.pos.y)

    # find closest point on rectangle
    closest_point = [point[0], point[1]]
    for dim in range(2):
        # inside case
        if abs(point[dim] - surface_center[dim]) < (size[dim] / 2):
            pass
        # to the left case
        elif point[dim] - surface_center[dim] < 0:
            closest_point[dim] = surface_center[dim] - (size[dim] / 2)
        # to the right case
        elif point[dim] - surface_center[dim] > 0:
            closest_point[dim] = surface_center[dim] + (size[dim] / 2)

    # project back into 3d
    closest_point_3d = vp.vec(0,0,0)
    if electrode.orientation == 'x':
        closest_point_3d = vp.vec(electrode.object.pos.x, closest_point[0], closest_point[1])
    elif electrode.orientation == 'y':
        closest_point_3d = vp.vec(closest_point[0], electrode.object.pos.y, closest_point[1])
    elif electrode.orientation == 'z':
        closest_point_3d = vp.vec(closest_point[0], closest_point[1], electrode.object.pos.z)

    return closest_point_3d



def find_electric_field(pos, charged_objects):
    electric_field = vp.vec(0,0,0)
    for object in charged_objects:
        closest_pos = find_closest_point(pos, object)
        distance = find_distance(pos, closest_pos)
        mag = (K * object.charge) / (distance ** 2)
        vec_to_obj = closest_pos - pos
        
        ratio = mag / distance
        indv_field = vec_to_obj * ratio
        electric_field += indv_field

    return electric_field



def main():
    cathode = Electrode(pos=vp.vec(0,0,0), charge=0, size=(2,2), orientation='x')

    accelerating_anodes = [
        #Electrode(pos=vp.vec(10,0,0), charge=1e-8, size=(2,2), orientation='x', color=vp.color.red),

        # accelerating
        Electrode(pos=vp.vec(20,-3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(20,3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(20,0,-3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),
        Electrode(pos=vp.vec(20,0,3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),

        Electrode(pos=vp.vec(25,-3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(25,3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(25,0,-3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),
        Electrode(pos=vp.vec(25,0,3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),

        Electrode(pos=vp.vec(30,-3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(30,3,0), charge=1e-8, size=(2,2), orientation='y', color=vp.color.red),
        Electrode(pos=vp.vec(30,0,-3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),
        Electrode(pos=vp.vec(30,0,3), charge=1e-8, size=(2,2), orientation='z', color=vp.color.red),

        # steering
        Electrode(pos=vp.vec(35,-8,0), charge=3e-9, size=(2,2), orientation='y', color=vp.color.red),
        #Electrode(pos=vp.vec(25,5,0), charge=1e-9, size=(2,2), orientation='y', color=vp.color.red),
        #Electrode(pos=vp.vec(25,0,-5), charge=1e-9, size=(2,2), orientation='z', color=vp.color.red),
        Electrode(pos=vp.vec(35,0,8), charge=3e-9, size=(2,2), orientation='z', color=vp.color.red),
    ]

    electrons = [Electron(vp.vec(1,0,0)), Electron(vp.vec(4,1,0))]

    vp.scene.autoscale = False
    vp.scene.camera.pos = vp.vec(25,0,0)
    tickspeed = 5e-8
    tickNum = 0
    screen_distance = 45
    # main loop
    while True:
        vp.rate(60)
        tickNum += 1
        # create electrons
        if tickNum > 30:
            tickNum = 0
            electrons.append(Electron(pos=vp.vec(1, (random.random() - 0.5) / 2, (random.random() - 0.5) / 2)))
            print(len(electrons))

        # move all the stuff
        for electron in electrons:
            electron.tick(tickspeed, accelerating_anodes)

        # delete electrons out of range
        # TODO FORNEXTTIME: why the hell isn't this working???
        electrons = [electron for electron in electrons if electron.object.pos.x < screen_distance]


def test():
    cathode = Electrode(pos=vp.vec(0,0,0), charge=0, size=(2,2), orientation='x')
    anode = Electrode(pos=vp.vec(10,0,0), charge=1e-8, size=(2,2), orientation='x', color=vp.color.red)

    electron1 = Electron(vp.vec(1,0,0))

    closest_point1 = find_closest_point(electron1.object.pos, anode)
    test_arrow1 = vp.arrow(
            pos = electron1.object.pos,
            axis = closest_point1 - electron1.object.pos,
            shaftwidth = 0.1
            )

    electron2 = Electron(vp.vec(20,2,3))
    closest_point2 = find_closest_point(electron2.object.pos, anode)
    test_arrow2 = vp.arrow(
            pos = electron2.object.pos,
            axis = closest_point2 - electron2.object.pos,
            shaftwidth = 0.1
            )


main()
#test()
