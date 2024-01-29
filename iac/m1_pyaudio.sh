#!/bin/bash

poetry shell
pip uninstall -y pyaudio
arch -arm64 pip install --no-cache-dir --global-option='built_ext' --global-option='-I/opt/homebrew/include' --global-option='-L/opt/homebrew/lib' pyaudio==0.2.12
exit
