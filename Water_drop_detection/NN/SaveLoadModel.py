import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

from keras.models import model_from_json

def SaveModel(model, path: str, name: str):
    """
    Saves model and weights:

    Parameters
    ----------   
    model: segmentation_models.Unet
        The model to save

    path : str
        The path to save the model

    name : str
        File name without extension
    """

    with open(os.path.join(path, name + ".json"), "w") as json_file:
        model_json = model.to_json()
        json_file.write(model_json)

    model.save_weights(os.path.join(path, name + ".h5"))

def LoadModel(path, name: str, weights = None):
    """
    Load model and weights:

    Parameters
    ----------
    path : str
        The path to the model

    name : str
        File name without extension

    weights: str
        Weight name (if not the same as 'name')

    Returns
    ----------
    segmentation_models.Unet model with loaded weights
    """

    if weights is None:
        weights = name

    try:
        with open(os.path.join(path, name + ".json"), "r") as json_file:
            loaded_model_json = json_file.read()
            model = model_from_json(loaded_model_json)

        model.load_weights(os.path.join(path, weights + ".h5"))

    except FileNotFoundError:
        raise

    return model
