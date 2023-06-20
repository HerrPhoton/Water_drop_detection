from keras.models import model_from_json


def SaveModel(model, path, name):
    """Saves model and weights:
         #Arguments:
             model: the model to save
             path: path
             name: file name without extension
    """
    with open(path + "/" + name + ".json", "w") as json_file:
        model_json = model.to_json()
        json_file.write(model_json)
    model.save_weights(path + "/" + name + ".h5")


def LoadModel(path, name, weights=None):
    """Load model and weights:
         #Arguments:
             path: path
             name: file name without extension
             weights: weight name (if not the same as 'name')
         #Returns:
             model
    """
    if weights is None:
        weights = name
    with open(path + "/" + name + ".json", "r") as json_file:
        loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
    model.load_weights(path + "/" + weights + ".h5")
    return model
