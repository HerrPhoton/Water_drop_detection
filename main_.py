import segmentation_models as sm

import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm
import tensorflow as tf
from keras.callbacks import CSVLogger
import SaveLoadModel
import BatchManager
import random
import addNoise

import keras
keras.backend.set_image_data_format('channels_last')


def main():
    BACKBONE = 'resnet50'
    preprocess_input = sm.get_preprocessing(BACKBONE)

    batchDir = "../batch"
    ext = ".npz"
    names = []
    def List_batch_names(batch_name):
        return [batch_name + "/" + x for x in BatchManager.Files_in_dir(os.path.join(batchDir, batch_name))]
    names += List_batch_names("orig")

    x_train, y_train = BatchManager.LoadMultipleBatches(batchDir, names)
    # x_val, y_val = BatchManager.LoadMultipleBatches(batchDir, List_batch_names("Anna 1")[::10])
    # x_val, y_val = BatchManager.LoadMultipleBatches(batchDir, [x + " valid" + ext for x in ["25_film", "28_film"]])

    # preprocess input
    x_train = preprocess_input(x_train)
    # x_val = preprocess_input(x_val)

    # define model
    # model = sm.Unet(BACKBONE, classes=3, activation='softmax', encoder_weights='imagenet')
    model = sm.Unet(BACKBONE, classes=2, activation='softmax', encoder_weights='imagenet')
    # model = SaveLoadModel.LoadModel("../model", "Anna 18 bg")   # continue train from this one

    optimizer = tf.keras.optimizers.Adam(3E-5)
    model.compile(
        optimizer,
        loss=sm.losses.bce_jaccard_loss,
        # loss=sm.losses.bce_dice_loss,
        metrics=[sm.metrics.iou_score],
    )

    model_name = "Sonya"

    csv_logger = CSVLogger("../model/" + model_name + ".log")
    save_model_val_best = tf.keras.callbacks.ModelCheckpoint(
        filepath="../model/" + model_name + '_best.h5',
        save_weights_only=True,
        monitor='iou_score',
        mode='max', save_best_only=True)

    with open("../model/" + model_name + "_best.json", "w") as json_file:
        json_file.write(model.to_json())


    def rotation_flip(img, seed):
        r = seed % 4
        f = (seed // 4) % 2
        if f:
            return np.rot90(np.flipud(img), r)
        else:
            return np.rot90(img, r)

    def my_generator_indexes(trainX, trainY, batch_size, indexes):
        sx = (batch_size,) + trainX.shape[1:]
        resultX = np.empty(sx, dtype=trainX.dtype)
        sy = (batch_size,) + trainY.shape[1:-1] + (2,)
        resultY = np.empty(sy, dtype=trainY.dtype)
        while True:
            for i in range(batch_size):
                index = np.random.choice(indexes)
                seed = random.randrange(8)
                resultX[i] = rotation_flip(trainX[index], seed)
                resultY[i] = rotation_flip(trainY[index], seed)

            yield resultX, resultY



    indexes_train = np.arange(len(x_train))
    batch_size = 20
    model.fit_generator(
        generator=my_generator_indexes(x_train, y_train, batch_size, indexes_train),
        steps_per_epoch=len(indexes_train) // batch_size,
        epochs=10000,
        verbose=1,
        callbacks=[csv_logger, save_model_val_best],
    )

    SaveLoadModel.SaveModel(model, "../model", model_name)


if __name__ == "__main__":
    main()
