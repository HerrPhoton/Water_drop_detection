import sys

import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pytest
from segmentation_models import Unet

from Water_drop_detection.NN.SaveLoadModel import *

##################################### Testing SaveModel #####################################
def test_SaveModel():
    model = Unet("resnet50", classes = 2, activation = 'softmax', encoder_weights = 'imagenet')
    SaveModel(model, ".", "test_model")

    assert os.path.isfile("test_model.json") and os.path.isfile("test_model.h5")

##################################### Testing LoadModel #####################################
def test_LoadModel():

    LoadModel(".", "test_model")

    os.remove("test_model.json")
    os.remove("test_model.h5")

def test_error_LoadModel():
    
    with pytest.raises(FileNotFoundError):
        LoadModel(".", "error_test")
