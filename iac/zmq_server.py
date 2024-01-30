
import os
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
sam_zeromq = ZeroMQWriter(topic='sam') # Everything from SAM will go out on topic IASR

debug = DebugModule()

zmq_cozmo_cam_read = ZeroMQReader(topic="cozmo")
zmq_cozmo_cam_read.subscribe(ztoi)
ztoi.subscribe(sam)
sam.subscribe(sam_zeromq)
sam.subscribe(debug)


zmq_cozmo_cam_read.run()
ztoi.run()
sam.run()
sam_zeromq.run()
debug.run()

print("Running pipeline")
input()

zmq_cozmo_cam_read.stop()
ztoi.stop()
sam.stop()
sam_zeromq.run()
debug.stop()