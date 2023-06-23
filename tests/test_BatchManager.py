import sys

from os.path import dirname, join, abspath
sys.path.insert(0, abspath(join(dirname(__file__), '..')))

import pytest
import numpy as np

from src.NN.BatchManager import *

##################################### Testing natural_sorting #####################################
@pytest.mark.parametrize("lst, res",
                         [(['1', '4', '10', '3'], ['1', '10', '3', '4']),
                          (['1', '2', '3', '4'], ['1', '2', '3', '4']),
                          (['a100', 'a5', 'a', 'a1'], ['a', 'a1', 'a100', 'a5'])])
def test_natural_sorting(lst, res):
    assert natural_sorting(lst) == res

def test_error_natural_sorting():

    with pytest.raises(TypeError):
        natural_sorting(["1", "2", 4])

##################################### Testing Files_in_dir #####################################
@pytest.mark.parametrize("dir, mask, res",
                         [("tests/imgs", "", ["img0000.jpg", "img0001.jpg", "img0002.jpg"]),
                          ("tests/imgs", "img", ["img0000.jpg", "img0001.jpg", "img0002.jpg"]),
                          ("tests/imgs", "png", [])])
def test_Files_in_dir(dir, mask, res):
    assert Files_in_dir(dir, mask) == res

def test_error_Files_in_dir():

    with pytest.raises(FileNotFoundError):
        Files_in_dir('error')

##################################### Testing Open_Images #####################################
@pytest.mark.parametrize("lst, cnt",
                         [(["img0000.jpg", "img0001.jpg", "img0002.jpg"], 3),
                          ([], 0)])
def test_Open_Images(lst, cnt):
    assert len(Open_Images('tests/imgs', lst)) == cnt

@pytest.mark.parametrize("path, names, error",
                         [('error', [], FileNotFoundError),
                          ('tests/imgs', ["img0000.jpg", 4], TypeError)])
def test_error_Open_Images(path, names, error):

    with pytest.raises(error):
        Open_Images(path, names)

##################################### Testing SaveBatch #####################################
def test_SaveBatch():

    SaveBatch(np.zeros(3), np.zeros(3), '.', 'test.npz')
    assert os.path.isfile('test.npz')

    os.remove('test.npz')

@pytest.mark.parametrize("x, y, path, name, error",
                         [(np.zeros(3), np.zeros(3), 'error', "test.npz", FileNotFoundError),
                          (np.zeros(3), np.zeros(3), '.', 1, TypeError)])
def test_error_SaveBatch(x, y, path, name, error):

    with pytest.raises(error):
        SaveBatch(x, y, path, name)

##################################### Testing LoadBatch #####################################
def test_LoadBatch():

    SaveBatch(np.zeros(3), np.zeros(3), '.', 'test.npz')
    x, y = LoadBatch('.', 'test.npz')

    assert np.array_equal(x, np.zeros(3)) and np.array_equal(y, np.zeros(3))

    os.remove('test.npz')

@pytest.mark.parametrize("path, name, error",
                         [('error', "test.npz", FileNotFoundError),
                          ('.', "1.npz", FileNotFoundError),
                          ('.', 1, TypeError)])
def test_error_LoadBatch(path, name, error):

    with pytest.raises(error):
        LoadBatch(path, name)
        
##################################### Testing LoadBatch #####################################
def test_LoadMultipleBatches():

    SaveBatch(np.zeros(3), np.zeros(3), '.', '1.npz')
    SaveBatch(np.zeros(3), np.zeros(3), '.', '2.npz')
    x, y = LoadMultipleBatches('.', ['1.npz', '2.npz'])

    assert np.array_equal(x, np.zeros(6)) and np.array_equal(y, np.zeros(6))

    os.remove('1.npz')
    os.remove('2.npz')

@pytest.mark.parametrize("path, name, error",
                         [('tests/imgs', ["1.npz", "2.npz"], FileNotFoundError),
                          ('error', ["1.npz", "2.npz"], FileNotFoundError),
                          ('.', 1, TypeError)])
def test_error_LoadMultipleBatches(path, name, error):

    with pytest.raises(error):
        LoadMultipleBatches(path, name)