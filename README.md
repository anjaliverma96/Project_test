For midproject submission


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
	 -	Story 1 : **Define the model objective** ~ why the model is being built and understand the end goal the model would achieve
	 -	Story 2 : **Gather the data** ~ Extract interaction matrix between users and jokes from the Jester dataset and transform data into format expected for a recommendation system
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




For midproject PR
Script that acquires data from data source and puts it into S3 is available in the src folder under downloaddata.py

To copy data from publicly accessible bucket "jokerecommender" to own private bucket, run:
python run.py loadS3 --bucket=
Script that creates database schema locally in sqlite is available in src folder under add_schema.py
2. To create the database in the location configured in config.py, run:
python run.py createSqlite

Script that creates database schema in RDS based on a configuration is available in src folder under add_schema.py
3. To create the database schema in AWS RDS, run:
python run.py createRDS

All variable declarations are in config.py