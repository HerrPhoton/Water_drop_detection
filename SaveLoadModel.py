from keras.models import model_from_json

def SaveModel(model, path, name):
    with open(path + "/" + name + ".json", "w") as json_file:
        model_json = model.to_json()
        json_file.write(model_json)
    model.save_weights(path + "/" + name + ".h5")

def LoadModel(path, name, weights=None):
    if weights is None:
        weights = name
    with open(path + "/" + name + ".json", "r") as json_file:
        loaded_model_json = json_file.read()
        model = model_from_json(loaded_model_json)
    model.load_weights(path + "/" + weights + ".h5")
    return model
