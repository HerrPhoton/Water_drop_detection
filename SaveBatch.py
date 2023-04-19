import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
# import tensorflow as tf
import SaveLoadModel
import BatchManager


def Open_extend_and_resize(file, final_size_wh, standard_size_wh, bg):
    try:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        assert img is not None
        img = BatchManager.pad_cut_image(img, standard_size_wh, bg)
        # plt.imshow(img), plt.show()
        data = cv2.resize(img, dsize=final_size_wh, interpolation=cv2.INTER_LINEAR)
        # plt.imshow(data), plt.show()
        return data
    except OSError as e:
        print("OSError. Bad img most likely", e, file)


def Batch_extend_and_resize(resultDir, dataDir, maskDir, img_postfix, mask_postfix, final_size_wh, standard_size_wh):
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    for img_file in tqdm(BatchManager.natural_sorting(os.listdir(dataDir))):
        if img_file.endswith(img_postfix):
            mask_file = img_file[:-len(img_postfix)] + mask_postfix
            data_array = Open_extend_and_resize(os.path.join(dataDir, img_file), final_size_wh, standard_size_wh, 255)
            mask_array = BatchManager.mask_image_to_hot_one(
                Open_extend_and_resize(os.path.join(maskDir, mask_file), final_size_wh, standard_size_wh, 0))
            BatchManager.SaveBatch(np.stack([data_array]), np.stack([mask_array]), resultDir,
                                   img_file[:-len(img_postfix)])


def Open_and_resize(file, IMG_SIZE):
    try:
        img = cv2.imread(file, cv2.IMREAD_COLOR)
        assert img is not None
        # plt.imshow(img_array), plt.show()
        data = cv2.resize(img, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
        # plt.imshow(data), plt.show()
        return data
    except OSError as e:
        print("OSError. Bad img most likely", e, file)


def Batch_resize(resultDir, dataDir, maskDir, img_postfix, mask_postfix, IMG_SIZE):
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    for img_file in tqdm(BatchManager.natural_sorting(os.listdir(dataDir))):
        if img_file.endswith(img_postfix):
            mask_file = img_file[:-len(img_postfix)] + mask_postfix
            data_array = Open_and_resize(os.path.join(dataDir, img_file), IMG_SIZE)
            mask_array = BatchManager.mask_image_to_hot_one(
                Open_and_resize(os.path.join(maskDir, mask_file), IMG_SIZE))
            BatchManager.SaveBatch(np.stack([data_array]), np.stack([mask_array]), resultDir,
                                   img_file[:-len(img_postfix)])


def Batch_cut(resultDir, dataDir, maskDir, img_postfix, mask_postfix, IMG_SIZE, BORDER):
    if not os.path.exists(resultDir):
        os.makedirs(resultDir)
    for img_file in tqdm(BatchManager.natural_sorting(os.listdir(dataDir))):
        if img_file.endswith(img_postfix):
            mask_file = img_file[:-len(img_postfix)] + mask_postfix
            data_array = BatchManager.generate_x_file(os.path.join(dataDir, img_file), IMG_SIZE, BORDER)
            mask_array = list(map(BatchManager.mask_image_to_hot_one,
                                  BatchManager.generate_x_file(os.path.join(maskDir, mask_file), IMG_SIZE, BORDER)
                                  ))
            BatchManager.SaveBatch(np.stack(data_array), np.stack(mask_array), resultDir,
                                   img_file[:-len(img_postfix)])

def process_chain_Ivan(folder, dataName):
    # dataDir = folder + dataName + "/noBackground"
    dataDir = folder + dataName + "/noBackground"
    maskDir = folder + dataName + "/mask"
    batchDir = "../batch"
    batch_resizedDir = "../batch_noBackground/Ivan/val/"
    # batch_resizedDir = "../batch_withBackground/Anna_new_data"
    result_resizedDir = os.path.join(batch_resizedDir, dataName)

    img_postfix = ".png"
    # img_postfix = ".bmp"
    mask_postfix = ".png"
    # mask_postfix = "_shell.bmp"

    IMG_SIZE = 32 * 8
    BORDER = 16 * 1

    Batch_resize(result_resizedDir, dataDir, maskDir, img_postfix,  mask_postfix, IMG_SIZE)


def process_chain(folder, dataName):
    dataDir = folder + dataName + "/new_data"
    maskDir = folder + dataName + "/masks_for_new_data"
    batchDir = "../batch"
    resultDir = os.path.join(batchDir, dataName)
    batch_resizedDir = "../batch_withBackground/Anna_new_data"
    result_resizedDir = os.path.join(batch_resizedDir, dataName)

    # img_postfix = ".png"
    img_postfix = ".bmp"
    # mask_postfix = ".png"
    mask_postfix = "_shell.bmp"

    IMG_SIZE = 32 * 8
    BORDER = 16 * 1

    Batch_extend_and_resize(result_resizedDir, dataDir, maskDir, img_postfix,  mask_postfix, final_size_wh=(256, 256), standard_size_wh=[1280, 1024])


class DropDataset():
    def __init__(self, folder, data_postfix, mask_postfix, transform=None):
        images = sorted([os.path.join(folder, name) for name
                         in os.listdir(folder) if name.endswith(data_postfix)])

        masks = sorted([os.path.join(folder, name) for name
                        in os.listdir(folder) if name.endswith(mask_postfix)])
        self.pairs = list(zip(images, masks))

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, index: int):
        # file path tuple
        img, mask = self.pairs[index]
        # read data as numpy array
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        mask = np.load(mask, allow_pickle=True)
        return img, mask

def visualize_samples(dataset, indices, title=None, count=10):
    # visualize random 10 samples
    plt.figure(figsize=(count * 3, 6))
    display_indices = indices[:count]
    if title:
        plt.suptitle("%s %s/%s" % (title, len(display_indices), len(indices)))
    for i, index in enumerate(display_indices):
        x, y = dataset[index]
        plt.subplot(2, count, i + 1)
        plt.imshow(x.squeeze())
        plt.grid(False)
        plt.axis('off')
        plt.subplot(2, count, i + 1 + count)
        plt.imshow(y.squeeze())
        plt.grid(False)
        plt.axis('off')

    plt.show()

IMG_SIZE = 32 * 8

def SaveToFile(dataset, resultDir, name):
    im_array = []
    mask_array = []
    for im, mask in dataset:
        im = cv2.resize(im, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR)
        mask = mask.astype("uint8")
        mask = cv2.resize(mask, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_NEAREST)
        class_zero = np.where(mask == 0)
        class_one = np.where(mask == 1)
        mask_hot_one = np.empty((IMG_SIZE, IMG_SIZE, 2))
        mask_hot_one[mask == 0] = [1, 0]
        mask_hot_one[mask == 1] = [0, 1]
        im_array.append(im)
        mask_array.append(mask_hot_one)

    BatchManager.SaveBatch(np.stack(im_array), np.stack(mask_array), resultDir,
                           name)

def main():
    orig_dataset = DropDataset("../data/C/data/", ".jpg", "_mask.jpg.npy")
    SaveToFile(orig_dataset, "../batch/orig", "orig")
    indices = np.random.choice(np.arange(len(orig_dataset)), 7, replace=False)
    visualize_samples(orig_dataset, indices, "Samples")

if __name__ == "__main__":
    main()
