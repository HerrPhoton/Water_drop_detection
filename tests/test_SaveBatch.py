import sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pytest
from Water_drop_detection.NN.SaveBatch import *

##################################### Testing DropDataset #####################################
def test_DropDataset():

    dataset = DropDataset('tests/dataset', '.jpg', '.npy')

    assert len(dataset) == 4 and len(dataset.__getitem__(0)) == 2

@pytest.mark.parametrize("dir, img_suf, mask_suf, error",
                         [('error', '.jpg', '.npy', FileNotFoundError),
                          ('tests/folder_with_junk', '.jpg', '.npy', Exception),
                          ('tests/folder_with_junk', '.png', '.npy', FileNotFoundError),
                          ('tests/folder_with_junk', '.jpg', '.png', FileNotFoundError)])
def test_error_DropDataset(dir, img_suf, mask_suf, error):

    with pytest.raises(error):
        DropDataset(dir, img_suf, mask_suf)

##################################### Testing SaveToFile #####################################
def test_SaveToFile():
    dataset = DropDataset('tests/dataset', '.jpg', '.npy')
    SaveToFile(dataset, '.', 'dataset')

    assert os.path.isfile('dataset.npz')

    os.remove('dataset.npz')

def test_error_SaveToFile():

    dataset = 42

    with pytest.raises(TypeError):
        SaveToFile(dataset, '.', 'dataset')