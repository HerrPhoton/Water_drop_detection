import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import BatchManager


class DropDataset():
    def __init__(self, folder, data_postfix, mask_postfix, transform=None):
        """Shows 10 images:
            #Arguments:
                 folder: folder path
                 data_postfix: end of files that will be images
                 mask_postfix: end of files that will be masks
                 transform: was in the example
        """
        images = sorted([os.path.join(folder, name) for name
                         in os.listdir(folder) if name.endswith(data_postfix)])

        masks = sorted([os.path.join(folder, name) for name
                        in os.listdir(folder) if name.endswith(mask_postfix)])
        self.pairs = list(zip(images, masks))

    def __len__(self):
        """Returns the number of elements
        """
        return len(self.pairs)

    def __getitem__(self, index: int):
        """Load image and mask:
            #Arguments:
                 index: pair number
            #Returns:
                 pair
        """
        # file path tuple
        img, mask = self.pairs[index]
        # read data as numpy array
        img = cv2.imread(img, cv2.IMREAD_COLOR)
        mask = np.load(mask, allow_pickle=True)
        return img, mask

def visualize_samples(dataset, indices, title=None, count=10):
    """Shows 10 images:
         #Arguments:
             dataset: an instance of the DropDataset class
             indices: order of indices to display
             title: image title
             count: the number to display
    """
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
    """Changes the size, convert the mask to binary and save
         #Arguments:
             dataset: an instance of the DropDataset class
             resultDir: folder path
             name: name
    """
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

    BatchManager.SaveBatch(np.stack(im_array), np.stack(mask_array), resultDir, name)

def main():
    orig_dataset = DropDataset("../data/C/data/", ".jpg", "_mask.jpg.npy")
    SaveToFile(orig_dataset, "../batch/orig", "orig")

    # orig_dataset = DropDataset("../data/C/data2/", ".png", "_mask.npy")
    # SaveToFile(orig_dataset, "../batch/orig", "orig2")

    indices = np.random.choice(np.arange(len(orig_dataset)), 7, replace=False)
    visualize_samples(orig_dataset, indices, "Samples")

if __name__ == "__main__":
    main()
