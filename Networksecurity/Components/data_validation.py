from Networksecurity.Entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Networksecurity.Entity.config_entity import DataValidationConfig
from Networksecurity.Exception.exception import NetworkSecurityException
from Networksecurity.Logging.logger import logging
from Networksecurity.Constants.training_pipeline import SCHEMA_FILE_PATH
from Networksecurity.Utils.main_utils.utils import read_yaml_file
from scipy.stats import ks_2samp  # checks 2 sample of data for data draft
import pandas as pd 
import os, sys



class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e: 
            raise NetworkSecurityException(e, sys)