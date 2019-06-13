# Joke Recommender 
## If you think an apple a day keeps the doctor away, try a joke!


## Index
<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Running the application](#running-the-application)
  * [1. Initial setup](#1-initial-setup)
  * [2. Set up environment](#2-set-up-environment)
  * [3. Download the data](#3-download-the-data)
  * [4. Initialize the database](#4-initialize-the-database)
  * [5. Launch App](#8-launch-app)
- [Make All](#make-all)
- [Testing](#testing)
- [Logging](#logging)

# Project Charter 

**Vision**: Engage people looking for entertainment and fun, in humor with jokes and content that match their interests. Help them discover jokes they might not have found otherwise and ultimately spread happiness by sharing jokes thereby increasing user base for the app.

**Mission**: Build an app for joke recommendations and drive app usage by enabling users to rank jokes on a visual analog scale. Produce updated recommendations based on their inputs(i.e. explicit preferences) using collaborative filtering(i.e. similarity to other users) recommendation model trained on Jester Dataset.

**Success criteria**: 
- Machine Learning Performance Metric : **AUC** - Area Under the ROC Curve that plots true
positive rate against false positive rate. This metric was chosen for model evaluation since we are concerned with whether users like the recommended joke or not rather than the accuracy of predicted user ratings for a joke. For the model to be successful, the goal would be to achieve a mean AUC score (across all users in test set) in the range 0.7 to 0.9 (though this is subject to change and can be ascertained only after optimizing/tuning model parameters ).

- Business Performance Metric : **Engagement** ~ measured by how frequently users come back to the app. Success is defined as having achieved a million plus downloads with 80% of the users visiting the app atleast once a day and is indicative of personalized recommendations that suit the sense of humor of the users.

# Planning
## Theme 1 : Joke Recommender
Recommendation system to gauge user preferences and make personalized joke suggestions, shared widely among users

 - **Epic 1** : **Model Building**
   -  Story 1 : **Define the model objective** ~ why the model is being built and understand the end goal the model would achieve
   -  Story 2 : **Gather the data** ~ Extract interaction matrix between users and jokes from the Jester dataset and transform data into format expected for a recommendation system
   - Story 3 : **Data Cleaning** ~ Handle any inconsistencies or missing values and prepare the data for modeling
   - Story 4 : **Feature Engineering** ~ Explore and create new attributes about the user-joke interaction that could potentially be used in the recommender
   - Story 5 : Split the data into **training** and **test** sets and train 2 different models
    -Story 5.1 : Train a **Baseline** model whose underlying algorithm is to recommend items that are popular
    -Story 5.2 : Train a **Collaborative Filtering** model using **Lightfm** package in python where the underlying algorithm is to suggest jokes that similar users like
   
 - **Epic 2** : **Model Selection and Evaluation**
   - Story 1 : Decide on loss functions and metrics to evaluate performance of the two models
   - Story 2 : Tune/Optimize model hyperparameters using cross-validation to arrive at the best fitted model
   - Story 3 : Evaluate each model using the decided metrics (such as AUC) using both the training and test datasets. Select the model with the best performance metric(highest AUC) for the test set

 - **Epic 3** : **Model Validation, Reproducibilty and Collaboration**
   - Story 1 : **Logging** ~ Manage complexity, communicate code to potential collaborators or developers, and debug software
   - Story 2 : Write **Unit Tests** and **Configure reproducibility tests** that can be run to test each stage of model development
   - Story 3 : **Version Control**: Create a Github repository for potential collaboration
   - Story 4 : **Documentation**: Make code readable and reproducible by documenting code     

## Theme 2 : Graphical User Interface
 - **Epic 1** : **Interface Development**
   - Story 1 : Develop a GUI to display the story
       - Visual analog scale : Slider from Less Fynny to Very Funny
       - Search bar to search for categories of jokes
       - Next and back buttons to cycle between jokes.
   - Story 2 : Test out the interface built with users and gather feedback on the initial iteration
   - Story 3 : Rework the suggestions from the users into the final step of the design and convert to a web page using HTML/CSS
- **Epic 2** : **Web App Deployment**
    - Story 1 : Introduce a backend by storing it on a server to fetch the data (probably MySQL db on AWS RDS)
   - Story 2 : Link the RDS to the front end app by deploying on a AWS EC2 server running a Flask app

  

# Backlog 

 - Theme1.Epic1.Story1 ***Define the model objective*** - 2 points    ***PLANNED***
 
 - Theme1.Epic1.Story2 ***Gather the data*** -  2 points    ***PLANNED***
 - Theme1.Epic1.Story3 ***Data Cleaning***  -  4 points  ***PLANNED***
 - Theme1.Epic1.Story4 ***Feature Engineering*** -  4 points  ***PLANNED***
 - Theme1.Epic1.Story5.1 ***Train Baseline Model***  - 4 points ***PLANNED***
 - Theme1.Epic1.Story5.2 ***Train Collaborative Filtering Model*** - 4 points ***PLANNED***
 - Theme1.Epic2.Story1 A ***Loss functions and metrics*** -  2 points
 - Theme1.Epic2.Story2 ***Optimize model hyperparameters*** -  4 points
 - Theme1.Epic2.Story3 ***Evaluate each model*** -  1 point
 - Theme1.Epic3.Story1 ***Logging*** -  4 points
 - Theme1.Epic3.Story2 ***Write and run tests***-   8 points
 - Theme1.Epic3.Story3 ***Version Control*** -   2 points
 - Theme1.Epic3.Story4 ***Documentation*** -   2 points
 - Theme2.Epic1.Story1 ***Develop a GUI***  -  4 points
 - Theme2.Epic2.Story1 - ***Fetch Data on AWS RDS***  - 4 points
 - Theme2.Epic2.Story2 - ***Deploy App on AWS EC2***  - 4 points


 
# Icebox  

 - Theme2.Epic1.Story2 - ***Test out interface***  
 - Theme2.Epic1.Story3 - ***Convert to webpage***  


## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── app.py                        <- Contains all the functionality of the flask app 
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging_local.conf            <- Configuration files for python loggers
│   ├── config.py                     <- Contains all configurations required for processing and set up
│   ├── flask_config.py               <- Contains all config required for the flask app
│
├── data                              <- Folder that stores the data downloaded from S3 bucket
│   
│
├── deliverables                      <- Contains midterm and final presentation
│
├── logs                              <- Contains execution logs
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development
│   ├── deliver                       <- Notebooks shared with others 
│   ├── archive                       <- Developed notebooks no longer being used 
│
├── src                               <- Contains all the scripts for the project
│   ├── archive/                      <- No longer current scripts.
│   ├── bototest                      <- Download data from s3 bucket to local.
│   ├── recommender.py                <- Script for helper functions to implement recommendation system 
│   ├── data_model.py                 <- Script for building the usage log database and injesting data
│
├── tests                             <- Contains files for unit testing
│
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
│
├── requirements.txt                  <- Python package dependencies 
│
├── Makefile                          <- Makefile to execute the make commands
```

## Running the application

Ths application can be run on both local system as well as on AWS. Steps on how to deploy the app for both settings is given below.

### 1. Initial Setup

Depending on where the app is deployed, ensure to go through the following:

#### Running on a local machine

**Specs**
* *Server: Local system*
* *Data Storage: Local filesystem*
* *Database: Local SQLite database*

**Makefile**
* Ensure that the `WHERE` variable is set to "Local"
* Ensure that the variable `BUCKET` is set to "Scripts" if running on Windows, else "bin" if on Linux or MacOS

**config/flask_config.py**
* Ensure that the `WHERE` variable is set to "Local"
* Ensure that the `HOST` variable is set to "127.0.0.1"
* Keep the default `PORT` of 3000; However, change it if this port is not available

**Setting up AWS CLI**
AWS CLI needs to be configured in your system for you to fetch the training data. Kindly refer to this [link](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) to set up the same  


#### Running on AWS

**Specs**
* *Server: EC2*
* *Data Storage: Local filesystem*
* *Database: RDS MySQL database provided by the user*

**RDS configurations**
In order to use RDS, the RDS credentials need to be added to the os environment. Add the following variables to the environment:
* MYSQL_USER : *Username to access the RDS instance*
* MYSQL_PASSWORD : *Password to access the RDS instance*
* MYSQL_HOST : *RDS instance endpoint*
* MYSQL_PORT : *Port number to access the instance*
* MYSQL_DB : *Name of the database*


**Makefile**
* Ensure that the `WHERE` variable is set to "AWS"
* Ensure that the variable `BUCKET` is set to "Scripts" if running on Windows server, else "bin" if on Linux server

**config/flask_config.py**
* Ensure that the `WHERE` variable is set to "AWS"
* Ensure that the `HOST` variable is set to "0.0.0.0"


### 2. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv housePrices

source housePrices/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n housePrices python=3.7.3
conda activate housePrices
pip install -r requirements.txt

```

#### With `Make`

```bash
make venv
```


### 3. Download the data

Original Data Source: 

Since the dataset used in this project for recommendation is relatively small, the data was downloaded directly during runtime from the S3 bucket to the local file system.

The bototest.py allows for this functionality


#### Running on Local
Run the following command in command line:
```bash
python run.py load_data
```

With `Make`
```
make load_data
```
Running this code will download the raw data from the s3 bucket and will put it in **/Data/raw/**


#### AWS
Run the following command in command line:
```bash
python run.py load_data --where=AWS --bucket=<destination_bucket_name>
```

With `Make`
```
make load_data
```
Running this code will download the raw data from the s3 bucket and will put it in **<destination_bucket_name>/raw/**


### 4. Initialize the database

#### Local
Run the following command in command line:
```bash
python run.py create_db
```

With `Make`
```
make create_db
```

Running this code will create a sqlite database to log the app usage at: **/Data/usage_log/msia423.db**

#### AWS

Run the following command in command line:
```bash
python run.py create_db --where=AWS
```

With `Make`
```
make create_db
```

Running this code will create the database specified in the given RDS instance 



### 5. Launch app

#### Local or AWS
Run the following command in command line:
```bash
python run.py run_app
``` 

With `Make`
```
make app
```
Running this code will start the flask app at the IP specified in **config/flask_config.py**

## Make All

In order to use Make All, please ensure that the [Initial Setup](#1-initial-setup) is complete

Run the following command in command line:
```
make all
```

## Testing

In order to unit test the functions, follow the following steps:
1. Navigate to the tests folder
2. Run the following command on the command line:
```
pytest test_recommender.py
```

## Logging
All logs are saved at **logs/logfile.log**











