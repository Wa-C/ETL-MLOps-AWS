from Networksecurity.Constants.training_pipeline import SAVED_MODEL_DIR, MODEL_FILE_NAME

import os, sys

from Networksecurity.Exception.exception import NetworkSecurityException
from Networksecurity.Logging.logger import logging

class NetworkModel:
    def __init__(self, preprocessor, model):

        try:
            self.preprocessor= preprocessor
            self.model= model
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def predict(self, x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat= self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)    