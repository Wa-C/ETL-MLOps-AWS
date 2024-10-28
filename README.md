# End-to-End MLOps Pipeline with AWS and Docker

## Overview

This project implements an end-to-end Machine Learning Operations (MLOps) pipeline integrating ETL processes, model training, validation, deployment, and continuous integration and deployment (CI/CD) using Docker and AWS services. The pipeline includes data ingestion from MongoDB, data validation, transformation, model training with hyperparameter tuning, and deployment using FastAPI. Continuous Integration and Deployment (CI/CD) is set up using GitHub Actions, enabling automatic building, testing, and deployment of the Docker container to AWS Elastic Container Registry (ECR) and running on an AWS EC2 instance.

## Features

- **Data Ingestion**: Fetching and storing data from MongoDB.
- **Data Validation**: Ensuring data quality and integrity using schema checks.
- **Data Transformation**: Preprocessing data for model training.
- **Model Training**: Training machine learning models with scikit-learn, including hyperparameter tuning.
- **Model Evaluation**: Evaluating model performance using classification metrics.
- **Model Deployment**: Deploying the model using FastAPI for real-time inference.
- **CI/CD Pipeline**: Automated build, test, and deployment using GitHub Actions.
- **Dockerization**: Containerizing the application for consistent deployment across environments.
- **AWS Integration**: Using AWS S3 for artifact storage, AWS ECR for Docker images, and AWS EC2 for deployment.
- **MLflow Tracking**: Experiment tracking and model registry using MLflow and DagsHub.
- **Batch Prediction**: Capability to process batch prediction requests.

## Technologies Used

- **Programming Language**: Python 3.x
- **Libraries**: scikit-learn, PyMongo, FastAPI, MLflow, dill, PyYAML
- **Database**: MongoDB
- **Containerization**: Docker
- **Cloud Services**: AWS S3, AWS ECR, AWS EC2
- **CI/CD**: GitHub Actions
- **Experiment Tracking**: MLflow, DagsHub
- **Web Framework**: FastAPI

## Prerequisites

- Python 3.x installed on your local machine
- `pip` package manager
- Docker installed and running
- AWS account with access keys configured
- MongoDB database setup and accessible
- Git installed
- Virtual environment tool (`virtualenv` or `conda`)

## Folder Structure

```
EndToEndMLOpsAWSDocker/
├── .github/
│   └── workflows/
│       └── main.yaml
├── .gitignore
├── Network_Data/
├── Notebooks/
├── Networksecurity/
│   ├── __init__.py
│   ├── Components/
│   ├── Constants/
│   ├── Entity/
│   ├── Logging/
│   ├── Exception/
│   ├── Pipeline/
│   ├── Utils/
│   └── Cloud/
├── data_schema/
│   └── schema.yaml
├── main.py
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── setup.py
```


## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Wa-C/ETL-MLOps-AWS

cd EndToEndMLOpsAWSDocker
```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Required Packages

Upgrade setuptools and install dependencies:

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Set Up MongoDB

- Ensure that MongoDB is running and accessible.
- Update the MongoDB connection details in your configuration files or environment variables.

### 5. Configure AWS Credentials

Install AWS CLI:

```bash
pip install awscli
```

Configure AWS CLI with your credentials:

```bash
aws configure
```

### 6. Set Up MLflow Tracking

Install MLflow:

```bash
pip install mlflow
```

Run MLflow UI:

```bash
mlflow ui
```

### 7. Update Configuration Files

- Update `config_entity.py` and other configuration files with the correct paths and parameters as per your environment.
- Ensure that `schema.yaml` reflects the correct data schema for validation.

## Usage

### Running the Pipeline Locally

#### **Data Ingestion**

Run `main.py` to start the data ingestion process:

```bash
python main.py
```

#### **Model Training and Evaluation**

The `main.py` script will automatically proceed through data validation, transformation, and model training steps.

#### **Running the FastAPI Application**

Start the FastAPI server:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the API documentation at `http://localhost:8000/docs`.

#### **Triggering the Pipeline via API**

Send a GET request to the `/train` endpoint to start the training pipeline:

```bash
http://localhost:8000/train
```

#### **Making Predictions**

Use the `/predict` endpoint to make predictions. You can submit data via a form or API request.

### Dockerization and Deployment

#### **Building Docker Image**

Build the Docker image:

```bash
docker build -t your-image-name:latest .
```

#### **Running Docker Container**

Run the Docker container:

```bash
docker run -p 8000:8000 your-image-name:latest
```

#### **Pushing Docker Image to AWS ECR**

Authenticate Docker to your default registry:

```bash
aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin aws_account_id.dkr.ecr.your-region.amazonaws.com
```

Tag the image:

```bash
docker tag your-image-name:latest aws_account_id.dkr.ecr.your-region.amazonaws.com/your-ecr-repo:latest
```

Push the image to ECR:

```bash
docker push aws_account_id.dkr.ecr.your-region.amazonaws.com/your-ecr-repo:latest
```

#### **Deploying on AWS EC2**

- SSH into your EC2 instance.
- Install Docker on the EC2 instance.
- Pull the Docker image from ECR.
- Run the Docker container on EC2.

## CI/CD Pipeline with GitHub Actions

The project includes a CI/CD pipeline configured using GitHub Actions. The workflow is defined in `.github/workflows/main.yaml`. It automates:

- Testing and linting the code.
- Building the Docker image.
- Pushing the Docker image to AWS ECR.
- Deploying the Docker container to AWS EC2.

### Setting Up CI/CD Pipeline

#### **AWS Credentials in GitHub Secrets**

Add the following secrets to your GitHub repository settings under **Settings > Secrets and variables > Actions**:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_REGION`
- `AWS_ECR_LOGIN_URI`
- `ECR_REPOSITORY_NAME`

#### **Self-Hosted Runner**

- Set up a self-hosted runner on your AWS EC2 instance following GitHub's instructions.
- Register the runner with your repository and configure it as per `main.yaml`.


## Pipeline Workflow

The pipeline consists of the following stages:

1. **Data Ingestion**: Data is ingested from MongoDB and stored locally.
2. **Data Validation**: The ingested data is validated against a predefined schema (`schema.yaml`).
3. **Data Transformation**: Data is preprocessed and transformed for model training.
4. **Model Training**: Multiple machine learning models are trained and evaluated using scikit-learn. Hyperparameter tuning is performed to select the best model.
5. **Model Evaluation**: The best model is evaluated using classification metrics.
6. **Model Deployment**: The selected model is serialized and saved. It is then deployed using FastAPI.
7. **Artifact Storage**: All artifacts, including models and data, are synced to AWS S3 for storage.
8. **CI/CD Pipeline**: GitHub Actions automate the testing, building, and deployment of the application.
9. **Dockerization**: The application is containerized using Docker for consistent deployment.
10. **Deployment to AWS**: Docker images are pushed to AWS ECR and deployed on an AWS EC2 instance.

## MLflow Experiment Tracking

MLflow is used to track experiments and model performance. Metrics and parameters are logged during model training, and the results can be visualized using the MLflow UI.

To view MLflow tracking:

```bash
mlflow ui
```

Alternatively, DagsHub can be integrated for remote experiment tracking.

## AWS Integration

- **AWS S3**: Used for storing artifacts such as models and data.
- **AWS ECR**: Stores Docker images built from the application.
- **AWS EC2**: Hosts the Docker container running the FastAPI application.

## FastAPI Application

The FastAPI application serves two main endpoints:

- **`/train`**: Triggers the entire training pipeline.
- **`/predict`**: Accepts data input and returns predictions.

### Running the FastAPI Application

Start the server with:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Access the API documentation at `http://localhost:8000/docs`.

## Batch Prediction

Batch prediction functionality allows the application to process large datasets and generate predictions in batch mode. Place your test data in the `valid_data` folder as `test.csv` (without the "result" column) and access the `/predict` endpoint.

## Security Considerations

- Ensure that sensitive information such as AWS credentials and database passwords are not hard-coded or committed to version control.
- Use environment variables or configuration files that are excluded from version control.

## Future Improvements

- Implement monitoring and logging for the deployed model.
- Integrate a frontend UI for easier interaction.
- Automate hyperparameter tuning with tools like Optuna.
- Set up alerting mechanisms for model performance degradation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Contact

For any questions or suggestions, please contact [syedwassiulhaque@gmail.com].

---

