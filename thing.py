import vpython as vp
import math
import random

K = 9e9 # Nm^2/C

MIN_ELECTRODE_CHARGE = 1e-10 # these are kinda arbitrary
MAX_ELECTRODE_CHARGE = 2e-8

class Electron:
    def __init__(self, pos):
        self.velocity = vp.vec(0.1,0,0) # m/s
        self.charge = 1.6e-19 # C
        self.mass = 9.1e-31 # kg
        self.object = vp.sphere(
                pos=pos, # m
                radius=0.2, # just for illustrative purposes
                color=vp.color.yellow)
        self.tick_num = 0
        self.is_dead = False
        self.is_moving = True

    def tick(self, charged_objects, tickspeed):
        if self.is_moving:
            # get force
            electric_field = find_electric_field(self.object.pos, charged_objects) # N/C
            force = self.charge * electric_field # N
            accel = force / self.mass # m/s^2

            # update position
            self.velocity += accel * tickspeed
            self.object.pos += self.velocity * tickspeed

        self.tick_num += 1
        # die
        if self.tick_num > 500:
            self.is_dead = True
            self.die()


    # hacky way to "delete" an electron
    def die(self):
        self.object.visible = False



class Electrode:
    def __init__(self, pos, charge, size, orientation, color=vp.vec(0.8,0.8,0.8), opacity_override=None):
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
                opacity=opacity_override if opacity_override else (charge - MIN_ELECTRODE_CHARGE) / (MAX_ELECTRODE_CHARGE - MIN_ELECTRODE_CHARGE))
        self.size = size # (m, m)
        self.orientation = orientation
        self.charge = charge # C
        self.opacity_override = opacity_override

    def set_charge(self, charge):
        self.charge = charge
        if not self.opacity_override:
            self.object.opacity = (charge - MIN_ELECTRODE_CHARGE) / (MAX_ELECTRODE_CHARGE - MIN_ELECTRODE_CHARGE)


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

    return electric_field # N/C



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


        # aquadag
        Electrode(pos=vp.vec(60,0,0), charge=8e-8, size=(20,20), orientation='x', color=vp.color.red, opacity_override=0.1)
    ]

    steering_anodes = [
        # n
        Electrode(pos=vp.vec(35,8,0), charge=1e-9, size=(2,2), orientation='y', color=vp.color.red),
        # s
        Electrode(pos=vp.vec(35,-8,0), charge=5e-9, size=(2,2), orientation='y', color=vp.color.red),
        # e
        Electrode(pos=vp.vec(35,0,-8), charge=1e-9, size=(2,2), orientation='z', color=vp.color.red),
        # w
        Electrode(pos=vp.vec(35,0,8), charge=5e-9, size=(2,2), orientation='z', color=vp.color.red),
    ]

    all_anodes = accelerating_anodes + steering_anodes

    electrons = [Electron(vp.vec(1,0,0)), Electron(vp.vec(4,1,0))]

    def set_steer_electrode(event, electrode_num):
        print(event.value)
        new_charge = (event.value * (MAX_ELECTRODE_CHARGE - MIN_ELECTRODE_CHARGE)) + MIN_ELECTRODE_CHARGE
        steering_anodes[electrode_num].set_charge(new_charge) 

    label_n = vp.wtext(text="N")
    steer_n = vp.slider(bind=lambda event: set_steer_electrode(event, 0), min=0, max=1, length=200)

    label_s = vp.wtext(text="S")
    steer_s = vp.slider(bind=lambda event: set_steer_electrode(event, 1), min=0, max=1, length=200)

    label_e = vp.wtext(text="E")
    steer_e = vp.slider(bind=lambda event: set_steer_electrode(event, 2), min=0, max=1, length=200)

    label_w = vp.wtext(text="W")
    steer_w = vp.slider(bind=lambda event: set_steer_electrode(event, 3), min=0, max=1, length=200)

    vp.scene.autoscale = False
    vp.scene.camera.pos = vp.vec(25,0,0)
    tickspeed = 5e-8
    tick_num = 0
    screen_distance = 55
    # main loop
    while True:
        vp.rate(60)
        tick_num += 1
        # create electrons
        if tick_num % 5 == 0:
            electrons.append(Electron(pos=vp.vec(1, (random.random() - 0.5) / 4, (random.random() - 0.5) / 4)))

        # move all the stuff
        for electron in electrons:
            electron.tick(charged_objects=all_anodes, tickspeed=tickspeed)

        # stop electrons at the screen
        for electron in electrons:
            if electron.object.pos.x >= screen_distance:
                electron.is_moving = False
        
        # delete electrons out of range (this is kinda hacky...)
        electrons = [electron for electron in electrons if electron.is_dead == False]


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
