
import os
os.environ['COZMO'] = "/Users/catherinehenry/Dev/cozmo-python-sdk-fork/src"

from ZeroMQto import ZeroMQto
from retico_core.debug import DebugModule
from retico_zmq import ZeroMQReader, ReaderSingleton
from retico_sam.hfsam import SAMModule


idk = ZeroMQto()


ReaderSingleton(ip='192.168.1.212', port='12346') # which ip and port?


sam = SAMModule(show=False, use_bbox=True)   # hugging face sam
debug = DebugModule()

cozmo_read = ZeroMQReader(topic="cozmo")
cozmo_read.subscribe(idk)  # TODO: probably going to need something like "ZeroMQto____" to pass data to sam?
idk.subscribe(sam)
sam.subscribe(debug)


cozmo_read.run()
idk.run()
sam.run()
debug.run()


input()

cozmo_read.stop()
idk.stop()
sam.stop()
debug.stop()