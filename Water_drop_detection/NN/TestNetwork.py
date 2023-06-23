import math
import time
import os
from typing import List

from tqdm import tqdm
import pandas as pd
import numpy as np
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

import cv2

from . import SaveLoadModel
from . import BatchManager

def get_circle(arr: List):
    """
    Searches related areas and returns a list of dictionaries:
    
    Parameters
    ----------
    arr: Predicted mask

    Returns
    ----------
    list of dictionaries containing information about each related area

    x, y : int8
        Center of gravity

    size : int
        Area

    x_min, y_min, x_len, y_len : int
        Bounding box

    r : float
        Radius of the circle whose area is equal to the found area
    """

    if len(arr) == 0:
        raise ValueError

    inner = np.copy(arr)
    inner[inner != 1] = 0
    N, _, stats, centroids = cv2.connectedComponentsWithStats(inner.astype(np.int8))
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

def work(INPUTDIR: str, OUTPUTDIR: str, img_mask: str = ".png", mode: str = 'folder'):
    """
    Runs a neural network on new data:

    Parameters
    ----------   
    INPUTDIR : str
        Path to the folder with images

    OUTPUTDIR : str
        Path to save results

    img_mask : str
        Image suffix to process

    mode : str

        'folder' : Process a folder with images

        'picture' " Process an image
    """

    if INPUTDIR is None:
        INPUTDIR = "./water_drop_detection/NN/data/"

    if OUTPUTDIR is None:
        OUTPUTDIR = "./water_drop_detection/NN/output"

    os.makedirs(OUTPUTDIR, exist_ok = True)

    IMG_SIZE = 32 * 8

    if mode != "folder":
        original = [cv2.imread(os.path.join(INPUTDIR), cv2.IMREAD_COLOR)]
    else:
        original = BatchManager.Open_Images(INPUTDIR, BatchManager.Files_in_dir(INPUTDIR, img_mask))

    img_n = len(original)
    x_train = np.stack(list(map(lambda x: cv2.resize(x, dsize = (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_LINEAR), original)))

    model = SaveLoadModel.LoadModel("water_drop_detection/NN/model", "Model")

    start_time = time.time()
    predict = model.predict(x_train)
    print(f"--- predict {time.time() - start_time:.3f} seconds ---")

    count_img = list(range(0, img_n)) # for DataFrame
    areas_drops = []

    for i in tqdm(range(x_train.shape[0])):
        orig = original[i]
        mask = cv2.resize(predict[i], dsize = (orig.shape[1], orig.shape[0]), interpolation = cv2.INTER_CUBIC)
        mask = np.argmax(mask, 2)

        orig[mask == 1] = orig[mask == 1] * [0.5, 0.5, 0.5] + [127, 0, 0]
        circles = get_circle(mask)

        cv2.imwrite(os.path.join(OUTPUTDIR, str(i) + ".png"), orig)

        areas_drops_for_img = []

        for c in circles:
            cv2.rectangle(orig, (c['x_min'], c['y_min']), (c['x_min'] + c['x_len'], c['y_min'] + c['y_len']), (0, 0, 255), 1)

        for c in circles:
            orig = cv2.circle(orig, (int(c['x']), int(c['y'])), int(c['r']), [0, 255, 0], 1)
            orig[int(c['y']), int(c['x'])] = [0, 255, 0]
            areas_drops_for_img.append(c['size'])

        areas_drops.append(areas_drops_for_img)
        cv2.imwrite(os.path.join(OUTPUTDIR, str(i) + "_frame.png"), orig)
        
    df = pd.DataFrame({'Number of image' : count_img, 'Areas of drops': areas_drops})
    df.to_csv(os.path.join(OUTPUTDIR, "Areas.csv"), index = False)


# if __name__ == "__main__":
#     work("./src/NN/data", "./src/NN/output/", ".jpg")
