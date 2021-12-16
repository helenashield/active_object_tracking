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

def get_frame():
    folder = os.getcwd() + '/frames/'
    frame = bpy.context.scene.frame_current

    filepath = os.path.join(folder, "%d" %(frame))
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(use_viewport=True, write_still=True)


def suzanne(frame):
    objs = bpy.data.objects
    if 'Suzanne' in objs.keys():
        objs.remove(objs['Suzanne'], do_unlink=True)
    bpy.ops.mesh.primitive_monkey_add(size = 0.25)
    suzanne = bpy.context.object
    suzanne.location = (frame/25, 1, 1) 
    suzanne.rotation_euler = Euler((0, 0, math.radians(frame*10.0)), 'XYZ')

def my_very_complex_function(scene, context): # must take 2 arguments
    if scene.frame_current % 5 == 0:
        getframe(scene, context)
        objs = bpy.data.objects
        if 'Suzanne' in objs.keys():
             objs.remove(objs['Suzanne'], do_unlink=True) 
        bpy.ops.mesh.primitive_monkey_add(size = 0.25)
        suzanne = bpy.context.object
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


def add_camera():
    bpy.ops.object.camera_add()
    cam = bpy.context.selected_objects[0]
    cam.name = 'camera001'
    cam.data.name = cam.name
    cam.location = (5, -10, 1)  # 'camera_conf['location']'
    # cam.rotation_quaternion = (1, 0, 0, 0)  # camera_conf['rotation']
    cam.rotation_euler = Euler((math.radians(90.0), 0, 0), 'XYZ')
    cam.scale = (1, 1, 1)  # camera_conf['scale']
    cam.data.lens_unit = 'FOV'  # 'FOV' # 'MILLIMETERS'
    cam.data.angle = 0.69  # camera_conf['fov']
    cam.data.show_background_images = True

def remove_camera():
    cameras = bpy.data.cameras
    if 'camera.001' in cameras.keys():
        cameras.remove(cameras['camera001'], do_unlink=True)


#bpy.ops.screen.animation_play()
# remove the default items in blender
remove_default()

# add our camera
add_camera()

# add suzanne
suzanne(0)


# play 200 frames
for i in range(200):
    # let animation take a step
    bpy.context.scene.frame_set(i)

    # apply suzanne
    frame = bpy.context.scene.frame_current
    suzanne(frame)

    # save current frame
    cam = bpy.context.scene.objects['camera001']
    bpy.context.scene.camera = cam
    get_frame()
    print(frame)

#bpy.ops.screen.animation_cancel()

# remove camera 
remove_camera()







#bpy.app.handlers.frame_change_pre.append(my_very_complex_function)