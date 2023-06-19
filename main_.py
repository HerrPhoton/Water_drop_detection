import segmentation_models as sm
from keras.callbacks import CSVLogger
import tensorflow as tf
import SaveLoadModel
import BatchManager
import numpy as np
import os
import random
import keras


keras.backend.set_image_data_format('channels_last')


def main():
    BACKBONE = 'resnet50'
    BATCH_DIR = "../batch"
    MODEL_NAME = "Model"
    BATCH_SIZE = 10

    LR = 3E-5
    NEW_MODEL = False
    NAMES = []

    preprocess_input = sm.get_preprocessing(BACKBONE)

    def List_batch_names(batch_name):
        """Returns a list of paths to batches:
             #Arguments:
                 batch_name: batch folder name
             #Returns:
                 list of batch paths
        """
        return [batch_name + "/" + x for x in BatchManager.Files_in_dir(os.path.join(BATCH_DIR, batch_name))]
    NAMES += List_batch_names("orig")

    x_train, y_train = BatchManager.LoadMultipleBatches(BATCH_DIR, NAMES)
    x_train = preprocess_input(x_train)

    if NEW_MODEL:
        model = sm.Unet(BACKBONE, classes=2, activation='softmax', encoder_weights='imagenet')
    else:
        load_name = MODEL_NAME
        # model = tf.keras.models.load_model("../model/" + load_name + ".h5")
        model = SaveLoadModel.LoadModel("../model", load_name)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(LR),
        loss=sm.losses.bce_jaccard_loss,
        # loss=sm.losses.bce_dice_loss,
        metrics=[sm.metrics.iou_score],
    )

    csv_logger = CSVLogger("../model/" + MODEL_NAME + ".log")
    save_model_val_best = tf.keras.callbacks.ModelCheckpoint(
        filepath="../model/" + MODEL_NAME + '_best.h5',
        save_weights_only=True,
        monitor='iou_score',
        mode='max', save_best_only=True)

    with open("../model/" + MODEL_NAME + "_best.json", "w") as json_file:
        json_file.write(model.to_json())

    def rotation_flip(img, seed):
        """Rotates and/or reflects the image:
             #Arguments:
                 img: numpy array
                 seed: action (seed % 4 number of 90 degree rotations,
                     (seed // 4) % 2 - presence of reflection
                     (0 1 2 3) - without reflection, (4 5 6 7) - with reflection)
             #Returns:
                 image
        """
        r = seed % 4
        f = (seed // 4) % 2
        if f:
            return np.rot90(np.flipud(img), r)
        else:
            return np.rot90(img, r)

    def my_generator_indexes(trainX, trainY, batch_size, indexes):
        """Used in fit_generator:
             #Arguments:
                 trainX: numpy array of images - datasetX
                 trainY: numpy array of images - datasetY
                 batch_size: size of returned batch
                 indexes: allowed indexes
             #Returns:
                 batch size batch_size
        """
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
    model.fit_generator(
        generator=my_generator_indexes(x_train, y_train, BATCH_SIZE, indexes_train),
        steps_per_epoch=len(indexes_train) // BATCH_SIZE,
        epochs=10000,
        verbose=1,
        callbacks=[csv_logger, save_model_val_best],
    )

    SaveLoadModel.SaveModel(model, "../model", MODEL_NAME)


if __name__ == "__main__":
    main()
