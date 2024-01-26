import sys, os
from enum import Enum

import time

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk-fork/src"

from retico_core.debug import DebugModule
from retico_dino.dino import Dinov2ObjectFeatures
from retico_vision.vision import ExtractObjectsModule
from retico_sam.hfsam import SAMModule
from retico_vision.vision import WebcamModule

# from retico_sam.sam import SAMModule

import tkinter
tk_root = tkinter.Tk()

class ModelCheckpoint(Enum):
    h = 'sam_vit_h_4b8939.pth'  # huge
    l = 'sam_vit_l_0b3195.pth'  # large
    b = 'sam_vit_b_01ec64.pth'  # base



    # path_var = ModelCheckpoint.b
    # path_var = 'mobile_sam.pt'

webcam = WebcamModule()

# sam = SAMModule(model=path_var.name, path_to_chkpnt=path_var.value, use_bbox=True) # fb sam
# sam = SAMModule(model='t', path_to_chkpnt=path_var, use_bbox=True) # mobile same
sam = SAMModule(show=False, use_bbox=True)   # hugging face sam
extractor = ExtractObjectsModule(num_obj_to_display=1)
feats = Dinov2ObjectFeatures(show=False, save=True, top_objects=1)
debug = DebugModule()

webcam.subscribe(sam)
sam.subscribe(extractor)
extractor.subscribe(feats)
feats.subscribe(debug)

webcam.run()
sam.run()
extractor.run()
feats.run()
debug.run()

print("Network is running")
input()

webcam.stop()
sam.stop()
extractor.stop()
debug.stop()

