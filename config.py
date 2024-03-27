import os
import yaml
from datetime import datetime


class ModelConfigs():
    def saveConfig(self, name: str = "configs.yaml"):
        if self.model_path is None:
            raise Exception("Model path is not specified")

        # create directory if not exist
        if not os.path.exists(self.model_path):
            os.makedirs(self.model_path)

        with open(os.path.join(self.model_path, name), "w") as f:
            yaml.dump(self.serialize(), f)

    def __init__(self):
        self.model_path = os.path.join("Models", datetime.strftime(datetime.now(), "%Y%m%d%H%M"))
        self.vocab = ""
        self.height = 50
        self.width = 200
        self.max_text_length = 0
        self.batch_size = 64
        self.learning_rate = 1e-3
        self.train_epochs = 300
        self.train_workers = 20

    def serialize(self):
        # get object attributes
        return self.__dict__

    @staticmethod
    def load(configs_path: str):
        with open(configs_path, 'r') as f:
            configs = yaml.load(f, Loader=yaml.FullLoader)

        config = ModelConfigs()
        for key, value in configs.items():
            setattr(config, key, value)

        return config