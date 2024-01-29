import base64

from PIL import Image

import retico_core
from retico_cozmorobot.cozmo_camera import CozmoCameraModule
from retico_vision import ImageIU
from retico_zmq import ZeroMQIU

import json

class ZeroMQto(retico_core.AbstractModule):

    """A Module for converting ZeroMQIU with PSI ASR to SpeechRecognitionIU

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
        return ImageIU

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
        img = Image.frombytes('RGB',  (320,240), bytearray(base64.b64decode(message)))
        output_iu = self.create_iu(None)
        output_iu.set_image(img, 1, 1)
        return retico_core.UpdateMessage.from_iu(output_iu, retico_core.UpdateType.ADD)


    def prepare_run(self):
        pass

    def shutdown(self):
        pass
