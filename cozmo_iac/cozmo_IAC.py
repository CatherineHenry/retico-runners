import asyncio
import os
import sys
import uuid
from datetime import datetime

import pickle

from retico_zmq import ZeroMQWriter, ZeroMQReader, WriterSingleton, ReaderSingleton, ZMQtoObjectFeatures

# set vars before importing modules
os.environ['YOLO'] = '/Users/catherinehenry/Dev/yolox'
os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk/src"
os.environ['EXPLAUTO'] = "/Users/catherinehenry/School/Thesis/explauto_fork/explauto"

from cozmo.util import degrees, Pose, Angle, distance_mm, speed_mmps
import warnings
warnings.filterwarnings('ignore')

import logging
logging.getLogger('tensorflow').setLevel(logging.ERROR)

#  Plotting
import tkinter
tk_root = tkinter.Tk()
import matplotlib
matplotlib.use('TkAgg')

#  Cozmo
sys.path.append(os.environ['COZMO'])
import cozmo
# from retico.modules.cozmo.cozmo_object_permanence import CozmoObjPermanenceModule
from retico_cozmorobot.cozmo_IAC import CozmoIntelligentAdaptiveCuriosityModule, ExperimentName

#  Misc Retico
from retico_core.debug import DebugModule
from retico_cozmorobot.cozmo_camera import CozmoCameraModule

# IP address of the machine running the writer singleton
# Whatever machine the writer is on is the IP you need for both server and client code
# Reminder: Singleton is making a static reference, so all the classes you instantiate refer to the same object
WriterSingleton(ip='192.168.1.212', port='12346')  # create ZeroMQ writer
# ReaderSingleton(ip='192.168.1.227', port='12348')  # IP of client receiving messages from (M1 Mac)
ReaderSingleton(ip='192.168.1.232', port='12348')  # IP of client receiving messages from (Desktop Linux)

def init_all(robot : cozmo.robot.Robot):
    max_turn_count = int(os.environ.get("MAX_TURN_COUNT", 0))
    execution_uuid = os.environ.get("EXECUTION_UUID") #"d3df72a1"
    experiment = ExperimentName[os.environ.get("EXPERIMENT", 'c').lower()].value
    save_data = True if os.environ.get("SAVE_DATA").lower() == "true" else False
    if save_data:
        print("SAVING DATA")
    else:
        print("NOT SAVING DATA")

    robot.set_robot_volume(0)
    ### Code to place cozmo imperfectly in center and have it center up itself. (similar logic to what we use in recentering later)
    #
    # cube = None
    # look_around = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    #
    # try:
    #     cube = robot.world.wait_for_observed_light_cube(timeout=60)
    # except asyncio.TimeoutError:
    #     print("Didn't find a cube :-(")
    #     return
    # finally:
    #     look_around.stop()
    #
    # # Cozmo will approach the cube he has seen
    # # using a 180 approach angle will cause him to drive past the cube and approach from the opposite side
    # # num_retries allows us to specify how many times Cozmo will retry the action in the event of it failing
    # action = robot.dock_with_cube(cube, approach_angle=cozmo.util.degrees(180), num_retries=2).wait_for_completed()
    #
    # robot.drive_straight(distance_mm(-275), speed_mmps(105), should_play_anim=False).wait_for_completed()
    # robot.turn_in_place(degrees(180), angle_tolerance=degrees(0), is_absolute=False, speed=Angle(2)).wait_for_completed()

    # Set Cozmo's head forward
    robot.set_head_angle(degrees(10), accel=10.0, max_speed=10.0, duration=1,
                         warn_on_clamp=True, in_parallel=True, num_retries=2).wait_for_completed()

    # robot.go_to_pose(Pose(350, 180, 0, angle_z=Angle(0)), relative_to_robot=False).wait_for_completed()
    #
    # Instantiate Modules
    #
    cozmo_cam = CozmoCameraModule(robot, exposure=0.7, gain=0.1)
    ztof = ZMQtoObjectFeatures()
    debug = DebugModule()

    cozmo_cam_zeromq = ZeroMQWriter(topic='cozmo')  # Everything from Cozmo Cam will go out on topic IASR
    sam_zmq_read = ZeroMQReader(topic='dino')

    # feats = ClipObjectFeatures(show=True, file_path=f"./IAC_output_data/images_detected_objs/{datetime.now().strftime('%m_%d')}")

    if execution_uuid:
        with open(f'./IAC_output_data/agent_{execution_uuid}.pickle', 'rb') as f:
            agent = pickle.load(f)
        date_timestamp = agent.execution_date_timestamp
        experiment = agent.experiment_name  # override experiment with whatever was used in the loaded model
        execution_uuid = agent.execution_uuid
        # TODO: this will need to be updated on the other machine :/
        # feats = ClipObjectFeatures(show=save_data, file_path=f"./IAC_output_data/images_detected_objs/{execution_uuid}")

    else:
        execution_uuid = str(uuid.uuid4()).split("-")[0]
        date_timestamp = datetime.now().strftime('%m_%d')
        agent = None
        # TODO: this will need to be updated on the other machine :/
        # feats = ClipObjectFeatures(show=save_data, file_path=f"./IAC_output_data/images_detected_objs/{execution_uuid}")

    cozmo_iac = CozmoIntelligentAdaptiveCuriosityModule(robot, tk_root=tk_root, date_timestamp=date_timestamp, agent=agent, save_data=save_data, experiment_name=experiment, execution_uuid=execution_uuid, max_turn_count=max_turn_count)
    debug = DebugModule()


    ## EXPLAUTO
    # We will use the left arm of the robot







    # The motors bounds for each one of the 2 treads
    # TODO: random numbers atm
    # curPos[0]=remote_control_cozmo.cozmo.pose.position.x
    # curPos[1]=remote_control_cozmo.cozmo.pose.position.y
    # m_mins = [-3, -5, -3] # forward, left, angle of rotation
    # m_maxs = [3, 5, 3] # forward, left, angle of rotation



    # m_mins = [0, -10, 0] # forward, left, angle of rotation
    # m_maxs = [0, 10, 0] # forward, left, angle of rotation
    #

    # reached_point = []
    #
    # for m in env.random_motors(n=3):
    #     print(f"random motor: {m}")
    #     reached_point.append(env.update(m))




    cozmo_iac.subscribe(cozmo_cam)  # Robot camera as input
    cozmo_cam.subscribe(cozmo_cam_zeromq) # Ship off for processing on GPU
    sam_zmq_read.subscribe(ztof)
    ztof.subscribe(cozmo_iac)
    ztof.subscribe(debug)

    cozmo_cam_zeromq.run()
    cozmo_cam.run()
    sam_zmq_read.run()
    ztof.run()
    cozmo_iac.run()
    debug.run()


    input() # keep everything running

    cozmo_cam_zeromq.run()
    cozmo_cam.run()
    sam_zmq_read.run()
    ztof.run()
    cozmo_iac.run()
    debug.run()

cozmo.run_program(init_all, tk_root=tk_root, use_viewer=True, use_3d_viewer=False, force_viewer_on_top=True)


