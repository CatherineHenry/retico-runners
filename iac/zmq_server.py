
import os

from retico_dino import Dinov2ObjectFeatures
from retico_vision import ExtractObjectsModule

os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk-fork/src"

from ZeroMQto import ZeroMQto
from retico_core.debug import DebugModule
from retico_zmq import ZeroMQReader, ReaderSingleton, WriterSingleton, ZeroMQWriter, ZMQtoImage
from retico_sam.hfsam import SAMModule


ztoi = ZMQtoImage()


ReaderSingleton(ip='192.168.1.212', port='12346')  # IP of client receiving messages from
# WriterSingleton(ip='192.168.1.227', port='12348')  # IP of client sending messages from (M1 Mac)
WriterSingleton(ip='192.168.1.232', port='12348')  # IP of client sending messages from (Linux Box)


sam = SAMModule(show=False, use_bbox=True)   # hugging face sam
dino_zeromq = ZeroMQWriter(topic='dino') # Everything from SAM will go out on topic IASR
extractor = ExtractObjectsModule(num_obj_to_display=1)
feats = Dinov2ObjectFeatures(show=False, save=True, top_objects=1)
debug = DebugModule()
zmq_cozmo_cam_read = ZeroMQReader(topic="cozmo")

zmq_cozmo_cam_read.subscribe(ztoi)
ztoi.subscribe(sam)
sam.subscribe(extractor)
extractor.subscribe(feats)
feats.subscribe(dino_zeromq)
feats.subscribe(debug)


zmq_cozmo_cam_read.run()
ztoi.run()
sam.run()
extractor.run()
feats.run()
dino_zeromq.run()
debug.run()

print("Running pipeline")
input()

zmq_cozmo_cam_read.stop()
ztoi.stop()
sam.stop()
extractor.stop()
feats.stop()
dino_zeromq.run()
debug.stop()
