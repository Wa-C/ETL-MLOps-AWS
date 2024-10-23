from Networksecurity.Components.data_ingestion import DataIngestion
from Networksecurity.Components.data_validation import DataValidation
from Networksecurity.Exception.exception import NetworkSecurityException
from Networksecurity.Logging.logger import logging
from Networksecurity.Entity.config_entity import DataIngestionConfig, DataValidationConfig
from Networksecurity.Entity.config_entity import TrainingPipelineConfig        
import sys

if __name__ == '__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)    
        logging.info("Initiate the data ingestion") 
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)

        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact, data_validation_config)
        logging.info("Initiate the data Validation") 
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("Data Validation Completed") 
        print(data_validation_artifact)
        

        
    except Exception as e:
        raise NetworkSecurityException(e, sys)    