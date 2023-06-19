import SaveLoadModel
import BatchManager
from tqdm import tqdm
import numpy as np
import cv2
import math
import os
import time

def get_circle(arr):
    """Searches related areas and returns a list of dictionaries:
         #Arguments:
             arr: image
         #Returns:
             list of dictionaries containing information about each related area
             x,y - center of gravity
             size - area
             x_min, y_min, x_len, y_len - bounding box
             r - radius of the circle whose area is equal to the found area
    """
    inner = np.copy(arr)
    inner[inner != 1] = 0
    N, labels, stats, centroids = cv2.connectedComponentsWithStats(inner.astype(np.int8))
    result = []
    for i in range(1, N):
        result.append({
            'x': centroids[i][0],
            'y': centroids[i][1],
            'size': int(stats[i][4]),
            'r': math.sqrt(stats[i][4] / math.pi),
            'x_min': int(stats[i][0]),
            'y_min': int(stats[i][1]),
            'x_len': int(stats[i][2]),
            'y_len': int(stats[i][3]),
        })
    return result


def work(INPUTDIR, OUTPUTDIR, img_mask=".png"):
    """Runs a neural network on new data:
         #Arguments:
             INPUTDIR: path to the folder with images
             OUTPUTDIR: path to save results
             img_mask: image suffix to process
    """
    if INPUTDIR is None:
        INPUTDIR = "../data"
    if OUTPUTDIR is None:
        OUTPUTDIR = "../output"

    os.makedirs(OUTPUTDIR, exist_ok=True)

    IMG_SIZE = 32 * 8

    original = BatchManager.Open_Images(INPUTDIR, BatchManager.Files_in_dir(INPUTDIR, img_mask))
    img_n = len(original)
    x_train = np.stack(list(map(lambda x: cv2.resize(x, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR), original)))

    model = SaveLoadModel.LoadModel("../model", "Model")

    start_time = time.time()
    predict = model.predict(x_train)
    print("--- predict %s seconds ---" % (time.time() - start_time))

    for i in tqdm(range(x_train.shape[0])):
        orig = original[i]
        mask = cv2.resize(predict[i], dsize=(orig.shape[1], orig.shape[0]), interpolation=cv2.INTER_CUBIC)
        mask = np.argmax(mask, 2)


        orig[mask == 1] = orig[mask == 1] * [0.5, 0.5, 0.5] + [127, 0, 0]
        circles = get_circle(mask)

        cv2.imwrite(OUTPUTDIR + "/" + str(i) + ".png", orig)
        for c in circles:
            cv2.rectangle(orig, (c['x_min'], c['y_min']), (c['x_min'] + c['x_len'], c['y_min'] + c['y_len']), (0, 0, 255), 1)
        for c in circles:
            orig = cv2.circle(orig, (int(c['x']), int(c['y'])), int(c['r']), [0, 255, 0], 1)
            orig[int(c['y']), int(c['x'])] = [0, 255, 0]

        cv2.imwrite(OUTPUTDIR + "/" + str(i) + "_frame.png", orig)

    end = 1


def main():
    work("../data/C/img/", "../output/", ".jpg")

if __name__ == "__main__":
    main()
