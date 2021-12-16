import math
import os
import sys
import json
import numpy as np
import argparse
from mathutils import Matrix, Quaternion, Euler, Vector
import mathutils
import bpy
import time
import sys
sys.path.insert(0, '/home/helena/Documents/Fall2021/8980/Project/blender-2.93.6-linux-x64/SiamMask/tools')
# from demo import init_mid_eval

def get_frame():
    # save from camera view
    folder = os.getcwd() + '/SiamMask/data/newframes/'
    frame = bpy.context.scene.frame_current
    filepath = os.path.join(folder, "%d" %(frame))
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(use_viewport=True, write_still=True)



    #save from bird view
    folder = os.getcwd() + '/otherview/'
    filepath = os.path.join(folder, "%d" %(frame))
    cam = bpy.context.scene.objects['camera002']
    bpy.context.scene.camera = cam
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(use_viewport=True, write_still=True)

def suzanne(frame):
    #objs = bpy.data.objects
    #if 'Suzanne' in objs.keys():
    #    objs.remove(objs['Suzanne'], do_unlink=True)
    #bpy.ops.mesh.primitive_monkey_add(size = 0.25)
    suzanne = bpy.data.objects['Suzanne']
    suzanne.location = (frame/25, math.cos(5*frame*math.pi/180), 1) 
    suzanne.rotation_euler = Euler((0, 0, math.radians(frame*10.0)), 'XYZ')

def movecam(frame):
    # get frame from experiments/siammask_sharp/newframe
    os.system("python SiamMask/tools/demo.py --config SiamMask/experiments/siammask_sharp/config_davis.json --resume SiamMask/experiments/siammask_sharp/SiamMask_DAVIS.pth --base_path SiamMask/data/newframes")

    orig_area = 60*85 # in pixels
    # read in estimated target size and location
    nextloc = np.loadtxt('newframes/nextloc%d.txt'%(frame+1))
    new_area = nextloc[1, 0]*nextloc[1, 1]
    x_offset = 960/2 - nextloc[0, 0]
    z_offset = 540/2 - nextloc[0, 1]
    y_offset = orig_area/new_area

    # convert to simulation units
    x_offset /= 400
    z_offset /= 400
    y_offset *= 6

    # move camera
    cam = bpy.data.objects['camera001']
    cam.location.x -= x_offset
    cam.location.y += (y_offset - 6)
    cam.location.z += z_offset
    cam.location.y = min(cam.location.y, 1)

    cam1 = bpy.data.objects['cam1']
    cam1.location = cam.location
    cam1.location.y -= 0.1

    #if 'camera001' in objs.keys():
    #bpy.ops.object.camera_add()
    #cam = bpy.context.selected_objects[0]
    #cam.name = 'camera001'
    #cam.data.name = cam.name
    #cam.location = (frame/25, math.cos(5*frame*math.pi/180)-5, 1)
    #cam1 = bpy.data.objects['cam1']
    #cam1.location = (frame/25, math.cos(5*frame*math.pi/180)-5.35, 1)
    #cam.rotation_euler = Euler((math.radians(90.0), 0, 0), 'XYZ')
    #cam.scale = (1, 1, 1)  # camera_conf['scale']
    #cam.data.lens_unit = 'FOV'  # 'FOV' # 'MILLIMETERS'
    #cam.data.angle = 0.69  # camera_conf['fov']
    #cam.data.show_background_images = True
    
    return new_area


def my_very_complex_function(scene, context): # must take 2 arguments
    if scene.frame_current % 5 == 0:
        getframe(scene, context)
        objs = bpy.data.objects
        #if 'Suzanne' in objs.keys():
        #     objs.remove(objs['Suzanne'], do_unlink=True) 
        #bpy.ops.mesh.primitive_monkey_add(size = 0.25)
        suzanne = bpy.data.objects['Suzanne']
        #suzanne = bpy.context.object
        suzanne.location = (scene.frame_current/25, 1, 1) 
    if scene.frame_current == 150:
        bpy.ops.screen.animation_cancel()

def remove_default():
    meshes = bpy.data.meshes
    lights = bpy.data.lights
    cameras = bpy.data.cameras

    # Remove the default objects
    if 'Cube' in meshes.keys():
        meshes.remove(meshes['Cube'], do_unlink=True)
    if 'Light' in lights.keys():
        lights.remove(lights['Light'], do_unlink=True)
    if 'Camera' in cameras.keys():
        cameras.remove(cameras['Camera'], do_unlink=True)
    if 'camera001' in cameras.keys():
        cameras.remove(cameras['camera001'], do_unlink=True)


def add_cameras():
    bpy.ops.object.camera_add()
    cam = bpy.context.selected_objects[0]
    cam.name = 'camera001'
    cam.data.name = cam.name
    cam.location = (0, -5, 1)  # 'camera_conf['location']'
    # cam.rotation_quaternion = (1, 0, 0, 0)  # camera_conf['rotation']
    cam.rotation_euler = Euler((math.radians(90.0), 0, 0), 'XYZ')
    cam.scale = (1, 1, 1)  # camera_conf['scale']
    cam.data.lens_unit = 'FOV'  # 'FOV' # 'MILLIMETERS'
    cam.data.angle = 0.69  # camera_conf['fov']
    cam.data.show_background_images = True

    bpy.ops.mesh.primitive_cone_add(radius1=0.3, radius2=0.05, depth=0.3)
    cone = bpy.context.selected_objects[0]
    cone.name = 'cam1'
    cone.data.name = cone.name
    cone.location = (0, -5.35, 1)
    cone.rotation_euler = Euler((math.radians(90.0), 0, 0), 'XYZ')

    bpy.ops.object.camera_add()
    cam2 = bpy.context.selected_objects[0]
    cam2.name = 'camera002'
    cam2.data.name = cam2.name
    cam2.location = (12, -10, 10)  # 'camera_conf['location']'
    # cam.rotation_quaternion = (1, 0, 0, 0)  # camera_conf['rotation']
    cam2.rotation_euler = Euler((math.radians(60.0), 0, math.radians(50.0)), 'XYZ')
    cam2.scale = (1, 1, 1)  # camera_conf['scale']
    cam2.data.lens_unit = 'FOV'  # 'FOV' # 'MILLIMETERS'
    cam2.data.angle = 0.87  # camera_conf['fov']
    cam2.data.show_background_images = True
    
   
    

def remove_camera():
    cameras = bpy.data.cameras
    if 'camera.001' in cameras.keys():
        cameras.remove(cameras['camera001'], do_unlink=True)
        cameras.remove(cameras['camera002'], do_unlink=True)


#bpy.ops.screen.animation_play()
# remove the default items in blender
remove_default()

# add our cameras
add_cameras()


# add suzanne
bpy.ops.mesh.primitive_monkey_add(size = 0.25)



# play 200 frames
for i in range(100):
    # let animation take a step
    bpy.context.scene.frame_set(i)

    # apply suzanne
    frame = bpy.context.scene.frame_current
    suzanne(frame)

    # save current frame
    cam = bpy.context.scene.objects['camera001']
    bpy.context.scene.camera = cam
    get_frame()

    
    # move camera
    movecam(frame)

#bpy.ops.screen.animation_cancel()

# remove camera 
remove_camera()







#bpy.app.handlers.frame_change_pre.append(my_very_complex_function)