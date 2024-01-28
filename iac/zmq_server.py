import os
from retico_core.debug import DebugModule
from retico_zmq import ZeroMQReader, ReaderSingleton
from retico_sam.hfsam import SAMModule

ReaderSingleton(ip='192.168.1.227', port='12346') # which ip and port?


sam = SAMModule(show=False, use_bbox=True)   # hugging face sam
debug = DebugModule()

cozmo_read = ZeroMQReader(topic="cozmo")
cozmo_read.subscribe(sam)  # TODO: probably going to need something like "ZeroMQto____" to pass data to sam?
sam.subscribe(debug)


cozmo_read.run()
sam.run()
debug.run()


input()

cozmo_read.stop()
sam.stop()
debug.stop()