import os 
import sys 
from Networksecurity.Exception.exception import NetworkSecurityException
from Networksecurity.Logging.logger import logging

from Networksecurity.Entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact
from Networksecurity.Entity.config_entity import ModelTrainerConfig

from Networksecurity.Utils.ml_utils.model.estimator import NetworkModel
from Networksecurity.Utils.main_utils.utils import save_object, load_object
from Networksecurity.Utils.main_utils.utils import load_numpy_array_data, evaluate_models
from Networksecurity.Utils.ml_utils.metric.classification_metric import get_classification_score

#ML algo import
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)



class ModelTrainer:
    def __init__(self, model_trainer_config:ModelTrainerConfig, data_transformation_artifact:DataTransformationArtifact):

        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def train_model(self, x_train, y_train,x_test,y_test):
        #initialization of models 
        models = {
            "Random Forest" : RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier(),

        }

        #HyperParameters tuning
        params = {
            "Decision Tree" : {
                'criterion': ['gini','entropy','log_loss'],
            #   'splitter' : ['best', 'random'],
            #   'max_features':['sqrt','log2'] 
            },
            "Random Forest":{
                #'criterion': ['gini','entropy','log_loss'],
                #'max_features':['sqrt','log2', None],
                'n_estimators':[8,16,32,64,128,256] 
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1, .01, .05, .001],
                'subsample': [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                #'criterion': ['squared_error','friedman_mse'],
                #'max_features':['auto','sqrt','log2'],
                'n_estimators':[8,16,32,64,128,256]
            },
            "Logistic Regression": {},
            "AdaBoost":{
                'learning_rate':[.1, .01, .05, .001],
                'n_estimators':[8,16,32,64,128,256]
            }
        }
        model_report:dict=evaluate_models(x_train=x_train,y_train=y_train,x_test=x_test,y_test=y_test,
                                          models=models,param=params)
        #To get best model score from dict (report={}   utils.py)
        best_model_score = max(sorted(model_report.values()))

        # To get best model name from the dict 

        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        best_model = models[best_model_name]

        y_train_pred = best_model.predict(x_train)

        classification_train_metric=get_classification_score(y_true=y_train, y_pred=y_train_pred)
        
        ## Track the mlflow 
        """  
        Code for MLflow will be here
        
        """

        y_test_pred = best_model.predict(x_test)
        classification_test_metric=get_classification_score(y_true=y_test, y_pred=y_test_pred)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path= os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)


        #Model Trainer Artifact

        model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                             train_metric_artifact=classification_train_metric,
                             test_metric_artifact=classification_test_metric,
                             )
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact


    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1], 
                train_arr[:, -1], #Taking last column
                test_arr[:, :-1],
                test_arr[:, -1] #Taking last column

            )

            model_trainer_artifact = self.train_model(x_train, y_train,x_test, y_test) #This function is defined above after creating this
            return model_trainer_artifact
        
        except Exception as e: 
            raise NetworkSecurityException(e, sys)    