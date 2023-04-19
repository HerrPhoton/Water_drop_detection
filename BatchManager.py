import math
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import re
from tqdm import tqdm

def natural_sorting(arr):
    convert = lambda text: int(text) if text.isdigit() else float('inf')
    arr.sort(key=lambda var: [[convert(x), x] for x in re.findall(r'-?[0-9]+|.', var)])
    return arr
# a = ["a2v", "a1v", "a20v", "a10v", "aa", "b", "ab", "a", "a-1v", "a0v", "axv"]
# natural_sorting(a)


def pad_cut_image(img, new_size_wh, background_color=0):
    assert len(img.shape) == 3
    # assert len(background_color.shape) == 1
    # assert background_color.shape[0] == img.shape[2]
    if [img.shape][0:2] == [new_size_wh[::-1]]:
        return img
    pad_y = new_size_wh[1] - img.shape[0]
    pad_x = new_size_wh[0] - img.shape[1]
    cut_y = max(-pad_y, 0)
    cut_x = max(-pad_x, 0)
    pad_y = max(pad_y, 0)
    pad_x = max(pad_x, 0)
    result = np.pad(img, ((pad_y // 2, (pad_y + 1) // 2), (pad_x // 2, (pad_x + 1) // 2), (0, 0)), constant_values=background_color)
    return result[cut_y // 2:result.shape[0] - (cut_y + 1) // 2, cut_x // 2:result.shape[1] - (cut_x + 1) // 2]
    # new_shape = (new_size[0], new_size[1], img.shape[2])
    # result = np.empty(shape=new_shape, dtype=img.dtype)
    # result[:, :] = background_color
    # return result

# img = cv2.imread("../data/Anna/1/noBackground/m_00002.png", cv2.IMREAD_COLOR)
# img2 = pad_cut_resize_image(img, [256, 1024], 255)
# plt.imshow(img2); plt.show()

def mask_image_to_hot_one(img):
    result = np.full((img.shape[0], img.shape[1], 3), 0, dtype=np.float32)
    result[:,:,2] = 1 #[0,0,1] by default
    index_black = np.where((img < [128,128,128]).all(axis=2))
    index_white = np.where((img >= [128,128,128]).all(axis=2))
    result[index_black] = [1,0,0]
    result[index_white] = [0,1,0]
    return result


def BACKUPsplit_image(img, frame_size=32 * 8, border=32):
    core_size = frame_size - 2 * border
    assert core_size > 0

    new_shape = list(img.shape)
    for i in range(2):
        new_shape[i] = frame_size
    extended_img = np.empty(new_shape, dtype=np.float32)
    # extended_img = np.empty(new_shape, dtype=np.uint8)
    s = (img.shape[0], img.shape[1])
    extended_img[border:border + s[0], border:border + s[1]] = img
    extended_img[border:border + s[0], 0:border] = extended_img[border:border + s[0], 2 * border:border:-1]
    extended_img[border:border + s[0], s[1] + border:] = extended_img[border:border + s[0], s[1] + border - 2:s[1] - core_size - 2:-1]
    extended_img[0:border, :] = extended_img[2 * border:border:-1, :]
    extended_img[s[0] + border:, :] = extended_img[s[0] + border - 2:s[0] - core_size - 2:-1, :]
    plt.imshow(extended_img); plt.show()

    result = []
    for y in range(0, img.shape[0], core_size):
        for x in range(0, img.shape[1], core_size):
            result.append(extended_img[y:y + frame_size, x:x + frame_size])
    return result


def split_image(img, frame_size=32 * 8, border=32):
    core_size = frame_size - 2 * border
    assert core_size > 0
    assert img.shape[0] + border > frame_size / 2
    assert img.shape[1] + border > frame_size / 2

    new_shape = list(img.shape)
    for i in range(2):
        if new_shape[i] < core_size:
            new_shape[i] = frame_size
        else:
            new_shape[i] += frame_size
    extended_img = np.empty(new_shape, dtype=np.float32)
    # extended_img = np.empty(new_shape, dtype=np.uint8)
    s = (img.shape[0], img.shape[1])
    extended_img[border:border + s[0], border:border + s[1]] = img
    extended_img[border:border + s[0], 0:border] = extended_img[border:border + s[0], 2 * border:border:-1]
    extended_img[border:border + s[0], s[1] + border:] = extended_img[border:border + s[0], s[1] + border - 2:2 * (s[1] + border) - 2 - new_shape[1]:-1]
    extended_img[0:border, :] = extended_img[2 * border:border:-1, :]
    extended_img[s[0] + border:, :] = extended_img[s[0] + border - 2:2 * (s[0] + border) - 2 - new_shape[0]:-1, :]
    # plt.imshow(extended_img); plt.show()

    result = []
    for y in range(0, img.shape[0], core_size):
        for x in range(0, img.shape[1], core_size):
            result.append(extended_img[y:y + frame_size, x:x + frame_size])
    return result

def unsplit_image(array, output_shape, frame_size, border):
    core_size = frame_size - 2 * border
    assert core_size > 0

    new_shape = list(output_shape)
    new_shape[0] += core_size
    new_shape[1] += core_size
    extended = np.empty(new_shape, array[0].dtype)
    i = 0
    for y in range(0, output_shape[0], core_size):
        for x in range(0, output_shape[1], core_size):
            extended[y:y + core_size, x:x + core_size] = array[i][border:border + core_size, border:border + core_size]
            i += 1
    return extended[:output_shape[0], :output_shape[1]]

def unsplit_image_average(array, output_shape, frame_size, border):
    core_size = frame_size - 2 * border
    assert core_size > 0

    new_shape = list(output_shape)
    new_shape[0] += frame_size
    new_shape[1] += frame_size
    extended = np.empty(new_shape, np.float64)
    count = np.empty(new_shape, np.float64)
    i = 0
    for y in range(0, output_shape[0], core_size):
        for x in range(0, output_shape[1], core_size):
            extended[y:y + frame_size, x:x + frame_size] += array[i]
            count[y:y + frame_size, x:x + frame_size] += 1
            i += 1
    extended[count>0] /= count[count>0]
    return np.asarray(extended[border:border + output_shape[0], border:border + output_shape[1]], dtype=array[0].dtype)


def generate_x_file(file, IMG_SIZE, BORDER):
    try:
        img_array = cv2.imread(file, cv2.IMREAD_COLOR)
        assert img_array is not None
        # plt.imshow(img_array), plt.show()
        data = split_image(img_array, IMG_SIZE, BORDER)
        return data
    except OSError as e:
        print("OSError. Bad img most likely", e, file)


def generate_x_folder(path, IMG_SIZE, BORDER, img_postfix=".png"):
    training_data = []
    n = 0
    for img in tqdm(natural_sorting(os.listdir(path))):
        if img_postfix is not None and img.endswith(img_postfix):
            training_data += generate_x_file(os.path.join(path, img), IMG_SIZE, BORDER)
            n += 1
    return np.stack(training_data).astype(np.float32), n


def generate_xy_folder(path, IMG_SIZE, BORDER, img_postfix="original.png", mask_postfix="fimal_mask.png"):
    training_data = []
    training_mask = []
    n = 0
    for img_file in tqdm(natural_sorting(os.listdir(path))):
        if img_file.endswith(img_postfix):
            mask_file = img_file[:-len(img_postfix)] + mask_postfix
            data_array = generate_x_file(os.path.join(path, img_file), IMG_SIZE, BORDER)
            training_data += data_array
            mask_array = map(mask_image_to_hot_one, generate_x_file(os.path.join(path, mask_file), IMG_SIZE, BORDER))
            training_mask += mask_array
            n += 1
    return np.stack(training_data), np.stack(training_mask), n  #np.stack(training_mask).astype(np.float32)


def Files_in_dir(dir_path, mask=""):
    return list(filter(lambda x: re.search(mask, x) is not None, natural_sorting(os.listdir(dir_path))))
    # result = []
    # for f in natural_sorting(os.listdir(dir_path)):
    #     if re.search(mask, f) is not None:
    #         result.append(f)
    # return result

def Open_Images(path, names):
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

# def generate_by_file_dict_list(file_dict_list, IMG_SIZE, BORDER):
#     for f in tqdm(file_dict_list):
#         yield np.stack(generate_x_file(f["x"], IMG_SIZE, BORDER)).astype(np.float32)


def SaveBatch(x, y, path, name):
    np.savez_compressed(os.path.join(path, name), x=x, y=y)

def LoadBatch(path, name):
    data = np.load(os.path.join(path, name))
    return data['x'], data['y']

def LoadMultipleBatches(path, names):
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
