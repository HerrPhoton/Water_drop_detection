import SaveLoadModel
import BatchManager
import cv2
import numpy as np
import math
import os
from tqdm import tqdm
import time


def get_mask(arr):
    arr = np.argmax(arr, 2)
    pic = np.empty((arr.shape[0], arr.shape[1], 3), dtype=np.int)
    pic[arr == 0] = np.array([0, 0, 0])
    pic[arr == 1] = np.array([255, 255, 255])
    pic[arr == 2] = np.array([255, 0, 0])
    return pic


def get_circle(arr):
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


def work(INPUTDIR, OUTPUTDIR, img_postfix=".png"):

    if INPUTDIR is not None:
        DATADIR = INPUTDIR
    if OUTPUTDIR is None:
        OUTPUTDIR = "../output"

    os.makedirs(OUTPUTDIR, exist_ok=True)

    IMG_SIZE = 32 * 8

    original = BatchManager.Open_Images(DATADIR, BatchManager.Files_in_dir(DATADIR, img_postfix))
    img_n = len(original)
    x_train = np.stack(list(map(lambda x: cv2.resize(x, dsize=(IMG_SIZE, IMG_SIZE), interpolation=cv2.INTER_LINEAR), original)))

    model = SaveLoadModel.LoadModel("../model", "Sonya")

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

    print("Graphs for" + INPUTDIR)

    end = 1


def main():
    work("../data/C/img/", "../output/", ".jpg")

if __name__ == "__main__":
    main()
