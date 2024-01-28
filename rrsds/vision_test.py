import sys, os

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

prefix = '/Users/catherinehenry/dev/catherine_retico/'
sys.path.append(prefix+'retico-core')
sys.path.append(prefix+'retico-vision')
sys.path.append(prefix+'retico-sam')
sys.path.append(prefix+'retico-dino')
sys.path.append(prefix+'retico-clip')

from retico_core import *
from retico_core.debug import DebugModule
from retico_vision.vision import WebcamModule 
from retico_dino.dino import Dinov2ObjectFeatures
from retico_vision.vision import ExtractObjectsModule
from retico_sam.sam import SAMModule
# from retico_clip.clip import ClipObjectFeatures

path_var = 'sam_vit_h_4b8939.pth'

webcam = WebcamModule()
sam = SAMModule(model='h', path_to_chkpnt=path_var, use_bbox=True)  
extractor = ExtractObjectsModule(num_obj_to_display=1)  
feats = Dinov2ObjectFeatures(show=False, top_objects=1)
# feats = ClipObjectFeatures(show=True)
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