from vpython import *

scene.title = "3D Object Builder"
scene.width = 900
scene.height = 600
scene.background = color.gray(0.15)

objects = []
object_names = []
selected_index = None

# COLOR HELPER
def get_color(name):
    name = name.lower()
    if name == "red": return color.red
    if name == "green": return color.green
    if name == "blue": return color.blue
    if name == "yellow": return color.yellow
    if name == "orange": return color.orange
    if name == "white": return color.white
    if name == "purple": return vector(0.6, 0, 0.8)
    print("Unknown color. Defaulting to white.")
    return color.white

# SHAPE CREATION FUNCTIONS
def add_gear():
    print("\n--- Create Gear ---")
    x = float(input("X position: "))
    y = float(input("Y position: "))
    z = float(input("Z position: "))
    radius = float(input("Radius: "))
    teeth_num = int(input("Number of teeth: "))
    col = get_color(input("Color: "))

    gear_parts = [] 

    thickness = radius * 0.2 
    
    hub = cylinder(pos=vector(x, y, z), axis=vector(0, 0, thickness), radius=radius, color=col)
    gear_parts.append(hub)

    # Teeth
    tooth_len = radius * 0.4
    tooth_width = (2 * pi * radius) / teeth_num * 0.5 
    
    for i in range(teeth_num):
        angle = (2 * pi / teeth_num) * i      
        tooth_x = x + radius * cos(angle)
        tooth_y = y + radius * sin(angle)        
        tooth_z = z + thickness / 2       
        t = box(pos=vector(tooth_x, tooth_y, tooth_z), size=vector(tooth_len, tooth_width, thickness), color=col)       
        t.rotate(angle=angle, axis=vector(0, 0, 1))      
        gear_parts.append(t)

    objects.append(gear_parts)
    object_names.append(f"Gear {len(objects)}")
    print("Gear created!")

def add_cube():
    print("\n--- Create Cube ---")
    x = float(input("X position: "))
    y = float(input("Y position: "))
    z = float(input("Z position: "))
    size = float(input("Size: "))
    col = get_color(input("Color: "))

    cube = box(pos=vector(x, y, z),
               size=vector(size, size, size),
               color=col)

    objects.append(cube)
    object_names.append(f"Cube {len(objects)}")
    print("Cube created!")

def add_sphere():
    print("\n--- Create Sphere ---")
    x = float(input("X position: "))
    y = float(input("Y position: "))
    z = float(input("Z position: "))
    radius = float(input("Radius: "))
    col = get_color(input("Color: "))

    sph = sphere(pos=vector(x, y, z),
                 radius=radius,
                 color=col)

    objects.append(sph)
    object_names.append(f"Sphere {len(objects)}")
    print("Sphere created!")

def add_cylinder():
    print("\n--- Create Cylinder ---")
    x = float(input("X position: "))
    y = float(input("Y position: "))
    z = float(input("Z position: "))
    radius = float(input("Radius: "))
    height = float(input("Height: "))
    col = get_color(input("Color: "))

    cyl = cylinder(pos=vector(x, y, z),
                   axis=vector(0, height, 0),
                   radius=radius,
                   color=col)

    objects.append(cyl)
    object_names.append(f"Cylinder {len(objects)}")
    print("Cylinder created!")

def add_cone():
    print("\n--- Create Cone ---")
    x = float(input("X position: "))
    y = float(input("Y position: "))
    z = float(input("Z position: "))
    radius = float(input("Radius: "))
    height = float(input("Height: "))
    col = get_color(input("Color: "))

    con = cone(pos=vector(x, y, z),
               axis=vector(0, height, 0),
               radius=radius,
               color=col)

    objects.append(con)
    object_names.append(f"Cone {len(objects)}")
    print("Cone created!")


# OBJECT SELECTION
def select_object():
    global selected_index

    print("\nAvailable objects:")
    for i, name in enumerate(object_names):
        print(f"{i}. {name}")

    try:
        selected_index = int(input("Enter object index to select: "))
        if selected_index < 0 or selected_index >= len(objects):
            print("Invalid index")
            selected_index = None
            return
        print(f"Selected: {object_names[selected_index]}")

    except:
        print("Invalid input")

# DELETE OBJECT
def delete_selected():
    global selected_index
    if selected_index is None:
        print("No object selected.")
        return
    obj = objects[selected_index]
    obj.visible = False
    del objects[selected_index]
    del object_names[selected_index]
    print("Object deleted.")
    selected_index = None

# KEYBOARD CONTROLS
def move_or_rotate(evt):
    if selected_index is None:
        return  
    key = evt.key
    obj = objects[selected_index]
    # If object is a gear, move each part
    def move_gear(dx, dy, dz):
        for part in obj:
            part.pos.x += dx
            part.pos.y += dy
            part.pos.z += dz

    def rotate_gear(angle, axis):
        # Rotate around the average center of gear
        center = vector(0,0,0)
        for part in obj:
            center += part.pos
        center /= len(obj)

        for part in obj:
            part.rotate(angle=angle, axis=axis, origin=center)

    # Check if this is a gear
    if isinstance(obj, list):
        if key == "left":  move_gear(-0.2, 0, 0)
        if key == "right": move_gear( 0.2, 0, 0)
        if key == "up":    move_gear(0, 0.2, 0)
        if key == "down":  move_gear(0, -0.2, 0)

        if key == "r":     rotate_gear(0.1, vector(0,0,1))
        if key == "t":     rotate_gear(0.1, vector(0,1,0))
        return
    # Normal objects 
    if key == "left":    obj.pos.x -= 0.2
    if key == "right":   obj.pos.x += 0.2
    if key == "up":      obj.pos.y += 0.2
    if key == "down":    obj.pos.y -= 0.2
    if key == "r":       obj.rotate(angle=0.1, axis=vector(0,0,1))
    if key == "t":       obj.rotate(angle=0.1, axis=vector(0,1,0))
scene.bind("keydown", move_or_rotate)

# MAIN MENU
while True:
    print("\n=========== 3D OBJECT BUILDER MENU ===========")
    print("1. Add Cube")
    print("2. Add Sphere")
    print("3. Add Cylinder")
    print("4. Add Cone")
    print("5. Add Gear")
    print("6. Select Object")
    print("7. Delete Selected Object")
    print("8. Exit")
    print("==============================================")

    choice = input("Choose option: ")

    if choice == "1": add_cube()
    elif choice == "2": add_sphere()
    elif choice == "3": add_cylinder()
    elif choice == "4": add_cone()
    elif choice == "5": add_gear()
    elif choice == "6": select_object()
    elif choice == "7": delete_selected()
    elif choice == "8":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")

    rate(60)
