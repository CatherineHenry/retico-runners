
import os
os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk-fork/src"

from ZeroMQto import ZeroMQto
from retico_core.debug import DebugModule
from retico_zmq import ZeroMQReader, ReaderSingleton, WriterSingleton, ZeroMQWriter
from retico_sam.hfsam import SAMModule


idk = ZeroMQto()


ReaderSingleton(ip='192.168.1.212', port='12346')  # IP of client receiving messages from
WriterSingleton(ip='192.168.1.212', port='12345')  # IP of client sending messages from


sam = SAMModule(show=False, use_bbox=True)   # hugging face sam
sam_zeromq = ZeroMQWriter(topic='sam') # Everything from SAM will go out on topic IASR

debug = DebugModule()

cozmo_read = ZeroMQReader(topic="cozmo")
cozmo_read.subscribe(idk)
idk.subscribe(sam)
sam.subscribe(sam_zeromq)
sam.subscribe(debug)


cozmo_read.run()
idk.run()
sam.run()
sam_zeromq.run()
debug.run()


input()

cozmo_read.stop()
idk.stop()
sam.stop()
sam_zeromq.run()
debug.stop()