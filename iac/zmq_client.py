from retico_zmq import ZeroMQWriter, WriterSingleton


import sys, os
from enum import Enum

import time
from cozmo.util import degrees

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk-fork/src"

from retico_core.debug import DebugModule
from retico_dino.dino import Dinov2ObjectFeatures
from retico_vision.vision import ExtractObjectsModule
# from retico_sam.sam import SAMModule
from retico_cozmorobot.cozmo_camera import CozmoCameraModule
import cozmo
import tkinter
tk_root = tkinter.Tk()

# IP address of the machine running the writer singleton
# Whatever machine the writer is on is the IP you need for both server and client code
# Reminder: Singleton is making a static reference, so all the classes you instantiate refer to the same object
WriterSingleton(ip='192.168.1.212', port='12346')  # create ZeroMQ writer
# Create new module for everything going to be sent to the server
def init_all(robot : cozmo.robot.Robot):
    robot.set_robot_volume(0)
    robot.set_head_angle(degrees(10), accel=10.0, max_speed=10.0, duration=1,
                         warn_on_clamp=True, in_parallel=True, num_retries=2).wait_for_completed()

    # path_var = ModelCheckpoint.b
    # path_var = 'mobile_sam.pt'

    cozmo_cam = CozmoCameraModule(robot, exposure=0.45, gain=0.03)

    # sam = SAMModule(model=path_var.name, path_to_chkpnt=path_var.value, use_bbox=True) # fb sam
    # sam = SAMModule(model='t', path_to_chkpnt=path_var, use_bbox=True) # mobile same
    # extractor = ExtractObjectsModule(num_obj_to_display=1)
    # feats = Dinov2ObjectFeatures(show=False, save=True, top_objects=1)
    # debug = DebugModule()

    cozmo_cam_zeromq = ZeroMQWriter(topic='cozmo') # Everything from Cozmo Cam will go out on topic IASR

    cozmo_cam.subscribe(cozmo_cam_zeromq)
    # extractor.subscribe(feats)
    # feats.subscribe(debug)

    cozmo_cam.run()
    # sam.run()
    # extractor.run()
    # feats.run()
    # debug.run()

    print("Network is running")
    input()

    cozmo_cam.stop()
    # sam.stop()
    # extractor.stop()
    # debug.stop()

cozmo.run_program(init_all, tk_root=tk_root, use_viewer=True, use_3d_viewer=False, force_viewer_on_top=True)
