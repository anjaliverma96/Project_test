import os
import numpy as np
import pandas as pd
import random
import pymysql

from flask import Flask, url_for, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from config.settings import SQLALCHEMY_DATABASE_URI

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

from src.data_model import Ratings_Log
from src.recommender import Recommender
from src.bototest import Boto

import logging
import logging.config
logger = logging.getLogger()

app = Flask(__name__)
app.secret_key = 'verysecretsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)




################ ROUTES

@app.route('/', methods = ['GET','POST'])
def home():
    

    """ This route renders the homepage of the app

    args : 
        None
    returns :
        renders home.html

    """
    logger.debug('Hit the home route')
    try: 


        fr = open(os.path.join("../data", "ratings.csv"), 'r') 
        fj = open(os.path.join("../data", "jokes.csv"), 'r')

        logger.debug('Hit the try block in home route')
    except FileNotFoundError: 
        
        logger.debug('Exception raised in home route')
        boto = Boto()
        boto.download_rating()
        boto.download_jokes()

    #Your system now has the files - rating.csv and jokes.csv in them

    ##
    #Check if the data is already in the RDS
    #if not then get it from S3 and put it into the RDS

    
    if request.method == 'GET':
        
        logger.debug('Home get method')
        return render_template('home.html')


@app.route('/jokes',methods = ['GET','POST'])
def recommend_joke():
    

    """This route is the main route which renders the joke recommendation

    Args:
        None

    Returns:

        recommend_jokes.html
    """

    logger.debug('Hit the recommend_joke route')

    logger.info('Reading the data files - ratings and joke ')
    data_raw = pd.read_csv('ratings.csv' ,index_col = 0)
    data_jokes = pd.read_csv('jokes.csv', index_col = 0)
    data_final = data_raw[:100000]

    logger.info('Finished reading the jokes and ratings file')
    

    reco = Recommender(data_final, data_jokes)
    
    res = reco.get_most_popular()
    joke = res[0]
    joke_num = res[1]


    
    if request.method == 'GET':
        
        #we will randomly select one of the highest rated joke and display it
        #insert code to get the joke

        session['joke_num'] = joke_num #this is default but you will need to get the joke number you are displaying
        session['prev_joke'] = joke
        logger.info('Added joke number and previous joke to session')
    
        return render_template('joke.html', joke= joke)
    
    else:

        logger.info('Post method of recommend joke hit')
        #This is the value which the user gave to the previous joke which is represented by joke_num
        value = request.form["rating"]
        session.pop('rating',None)

        #get the joke_num
        last_joke = session['joke_num']
        session.pop('joke_num',None)

        prev_joke = session['prev_joke']
        session.pop('prev_joke',None)

        #RDS ADD JOKE FOR FUTURE ANALYSIS
        add_data(prev_joke, value)
        logger.info('Data written to Database for future analysis')
        
    
        #now that we have the joke number we will create the svd with this information
        
        #check if session is set
        if 'user_pref' in session:
            logger.info('User preference in session - not a first time user')

            curr_user_pref = list(session['user_pref'])
            
            session.pop('user_pref',None)
            
            curr_user_pref[last_joke] = int(value)
            #fetch the data
            #create the matrix
            #append the user_pref
            #calculate svd
            
            #first we will get the interaction matrix
            interaction_df = reco.get_interaction()
            #append the user_pref
            new_df = reco.append_new_user(interaction_df, curr_user_pref)

            #calculate svd using the user_pref
            preds_df = reco.get_svd(new_df)

            #get the prediction

            recommended_res = reco.recommend_joke(preds_df,curr_user_pref)
            joke = recommended_res[0]
            joke_num= recommended_res[1]



            #set the sessions
            session['joke_num'] = joke_num
            session['user_pref'] = curr_user_pref
            session['prev_joke'] = joke
            
            return render_template('recommended_jokes.html', joke= joke)

        else :

            logger.info('User not preference in session - first time user')
            #first we will get the interaction matrix
            interaction_df = reco.get_interaction()

            #for that we will set a user_pref
            user_pref = [0]*interaction_df.shape[1] #create a list with the length of the number of jokes

            user_pref[last_joke] = int(value)
            
            
            #append the user_pref
            new_df = reco.append_new_user(interaction_df, user_pref)

            #calculate svd using the user_pref
            preds_df = reco.get_svd(new_df)



            #get the prediction

            recommended_res = reco.recommend_joke(preds_df,user_pref)
            joke = recommended_res[0]
            joke_num= recommended_res[1]

            new_joke = joke
            new_joke_number = joke_num #needs to be the one that is being recommend_joke
            
            #set the sessions
            session['joke_num'] = new_joke_number
            session['user_pref'] = user_pref
            session['prev_joke'] = joke




            return render_template('recommended_jokes.html', joke= new_joke)

#################### FUNCTION FOR ADDING DATA TO RDS
def add_data(joke, rating):


    """This function helps us add data to the RDS

    Args:
        joke : String which represents the joke string
        rating : Integer which is the rating given by the user

    Returns:
        None

    """
    #first we add the ratings data
    logger.info('Adding new data to RDS - add_data function called')
    try:
        joke_add = Ratings_Log(joke = joke,rating = rating)
        db.session.add(joke_add)
        db.session.commit()
    except:

        Logger.error("Could not write to database")
        logger.error(e)



#if __name__ == "__main__":
def run_app(args):
    app.run(host="0.0.0.0", port=80)
    debug = True
