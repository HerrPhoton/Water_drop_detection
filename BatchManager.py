from tqdm import tqdm
import numpy as np
import os
import cv2
import re


def natural_sorting(arr):
    """Sorts according to the order of the numbers:
         #Arguments:
             arr: array of strings
         #Returns:
             sorted array of strings
    """
    convert = lambda text: int(text) if text.isdigit() else float('inf')
    arr.sort(key=lambda var: [[convert(x), x] for x in re.findall(r'-?[0-9]+|.', var)])
    return arr
# a = ["a2v", "a1v", "a20v", "a10v", "aa", "b", "ab", "a", "a-1v", "a0v", "axv"]
# natural_sorting(a)


def Files_in_dir(dir_path, mask=""):
    """Returns a list of names of all files in alphabetical order containing mask in the name:
         #Arguments:
             dir_path: folder name
             mask: filter in the file name
         #Returns:
             list of names
    """
    return list(filter(lambda x: re.search(mask, x) is not None, natural_sorting(os.listdir(dir_path))))
    # result = []
    # for f in natural_sorting(os.listdir(dir_path)):
    #     if re.search(mask, f) is not None:
    #         result.append(f)
    # return result


def Open_Images(path, names):
    """Opens a list of images:
         #Arguments:
             path: folder path
             names: names of image files
         #Returns:
             image list
    """
    result = []
    for name in names:
        try:
            img = cv2.imread(os.path.join(path, name), cv2.IMREAD_COLOR)
            assert img is not None
            # plt.imshow(img_array), plt.show()
            result.append(img)
        except OSError as e:
            print("OSError. Bad img most likely", e, os.path.join(path, name))
    return result


def SaveBatch(x, y, path, name):
    """Stores two numpy arrays:
         #Arguments:
             x:image
             y:target
             path: folder path
             name: name, for example, 1.npz
    """
    np.savez_compressed(os.path.join(path, name), x=x, y=y)


def LoadBatch(path, name):
    """Loads two numpy arrays saved by the SaveBatch function:
         #Arguments:
             path: folder path
             name: name, for example, 1.npz
         #Returns:
             two numpy arrays image and target
    """
    data = np.load(os.path.join(path, name))
    return data['x'], data['y']


def LoadMultipleBatches(path, names):
    """Loads 2 * len(names) numpy arrays saved by the SaveBatch function:
         #Arguments:
             path: folder path
             name: array of names, e.g. ["1.npz", "2.npz"]
         #Returns:
             two numpy arrays image and target
    """
    size = 0
    shape_x = None
    shape_y = None
    type_x = None
    type_y = None
    for name in tqdm(names):
        x, y = LoadBatch(path, name)
        assert(x.shape[0] == y.shape[0])
        size += x.shape[0]
        assert(shape_x is None or shape_x == x.shape[1:])
        shape_x = x.shape[1:]
        assert(shape_y is None or shape_y == y.shape[1:])
        shape_y = y.shape[1:]
        assert(type_x is None or type_x == x.dtype)
        type_x = x.dtype
        assert(type_y is None or type_y == y.dtype)
        type_y = y.dtype
    result_x = np.empty((size,) + shape_x, dtype=type_x)
    result_y = np.empty((size,) + shape_y, dtype=type_y)
    current = 0
    for name in tqdm(names):
        x, y = LoadBatch(path, name)
        result_x[current : current + x.shape[0]] = x
        result_y[current : current + y.shape[0]] = y
        current += x.shape[0]
    return result_x, result_y
