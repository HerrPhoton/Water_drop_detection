import sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pytest
from Water_drop_detection.NN.TestNetwork import *

##################################### Testing get_circle #####################################
@pytest.mark.parametrize("dir, cnt", 
                         [("tests/folder_with_junk/img0000_mask.jpg.npy", 1),
                         ("tests/folder_with_junk/img0041_mask.jpg.npy", 16),
                         ("tests/folder_with_junk/zero_arr.npy", 0)])
def test_get_circle(dir, cnt):
    assert len(get_circle(np.load(dir))) == cnt

def test_error_get_circle():

    with pytest.raises(ValueError):
        get_circle(np.load("tests/folder_with_junk/error.npy"))