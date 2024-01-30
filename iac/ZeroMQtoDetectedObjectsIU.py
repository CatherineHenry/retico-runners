import base64

import numpy as np
from PIL import Image

import retico_core
from retico_vision import ImageIU, DetectedObjectsIU
from retico_zmq import ZeroMQIU

import json

class ZeroMQtoDetectedObjects(retico_core.AbstractModule):

    """A Module for converting ZeroMQIU with SAM to DetectedObjectsIU

    Attributes:

    """
    @staticmethod
    def name():
        return "idk Module"

    @staticmethod
    def description():
        return "A Module for converting Zero MQ json to a retico CozmoCam"

    @staticmethod
    def output_iu():
        return DetectedObjectsIU

    @staticmethod
    def input_ius():
        return [ZeroMQIU]

    def __init__(self, **kwargs):
        """Initializes the ZeroMQReader.

        Args: topic(str): the topic/scope where the information will be read.

        """
        super().__init__(**kwargs)

    def process_update(self, input_iu):
        '''
        This assumes that the message is json formatted, then packages it as payload into an IU
        '''
        message = input_iu._msgs[0][0].payload['message']
        image = input_iu._msgs[0][0].payload['image']
        img = Image.frombytes('RGB',  (320,240), bytearray(base64.b64decode(image)))
        output_iu = self.create_iu(None)
        # output_iu.set_detected_objects(img, np.array(json.loads(message)), "bb")
        output_iu.set_detected_objects(img, np.array(json.loads(message)), "seg")
        return retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)


    def prepare_run(self):
        pass

    def shutdown(self):
        pass
