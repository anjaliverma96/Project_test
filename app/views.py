
import numpy as np
import pandas as pd
import random
import pymysql
from flask import Flask, url_for, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from settings import SQLALCHEMY_DATABASE_URI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from recommender import Recommender
from bototest import Boto
import os

app = Flask(__name__)
app.secret_key = 'verysecretsecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)


########## DATA MODELS
class Jokes(db.Model):

    __tablename__ = 'jokesrecommended'

    id = Column(Integer,primary_key=True)
    joke = Column(String(400),unique=False)
    rating = Column(Integer, unique= False)

    def __repr__(self):
        jokes = "<Jokes(id='%i', user_id='%i', joke='%s', rating = '%i')>"
        return jokes % (self.id, self.user_id, self.joke, self.rating)



class UserRating(db.Model):

    """Create a data model for the database to be set up for capturing user input

    """

    __tablename__ = 'userrating'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=False)
    joke_id = Column(Integer, unique=False)
    rating = Column(Integer, unique=False)

    def __repr__(self):
        userrating_repr = "<UserRating(id='%i', user_id='%i', joke_id='%i', rating = '%i')>"
        return userrating_repr % (self.id, self.user_id, self.joke_id, self.rating)


class JokeDesc(db.Model):

    """Create a data model for the table JokeDesc

    """

    __tablename__ = 'jokedesc'

    joke_id = Column(Integer, primary_key=True)
    joke = Column(String(1000), unique=False, nullable=False)


    def __repr__(self):
        jokedesc_repr = "<JokeDesc(joke_id='%i', joke='%s')>"
        return jokedesc_repr % (self.joke_id, self.joke)


db.create_all()


################ ROUTES

@app.route('/', methods = ['GET','POST'])
def hello_world():
    

    

    #query the db to check if data is present 
    #if present then don't do anything
    #else get data from s3 boto to put into rds
    # data = User.query.all()
    # db.session.query()
    # if data:
    #     print('data is present')
    # else:
    #     print('data not present')
        
    #     # #add to db and print
    #     a = User(username = 'asdfa',email ='asdfsa@sdfs.com')
    #     db.session.add(a)
    #     db.session.flush()
    #     db.session.commit()


    #For direct calculation from s3

    #check if file is already present -
    #if not download
    try: 
        fr = open('ratings.csv', 'r') 
        fj = open('jokes.csv','r')
    except FileNotFoundError: 
    
        boto = Boto()
        boto.download_rating()
        boto.download_jokes()


    #Your system now has the files - rating.csv and jokes.csv in them

    ##
    #Check if the data is already in the RDS
    #if not then get it from S3 and put it into the RDS

    
    if request.method == 'GET':
        
        return render_template('home.html')


@app.route('/jokes',methods = ['GET','POST'])
def recommend_joke():
    '''
    session - user_pref, joke_num(0-19)
    '''
    #write code to get the first joke and compute the matrix
    #we have loaded the data
    data_raw = pd.read_csv('ratings.csv' ,index_col = 0)
    data_jokes = pd.read_csv('jokes.csv', index_col = 0)
    data_final = data_raw[:100000]

    #create an object of recommender
    reco = Recommender(data_final, data_jokes)
    
    res = reco.get_most_popular()
    joke = res[0]
    joke_num = res[1]


    
    if request.method == 'GET':
        
        #we will randomly select one of the highest rated joke and display it
        #insert code to get the joke

        session['joke_num'] = joke_num #this is default but you will need to get the joke number you are displaying
        session['prev_joke'] = joke
        return render_template('joke.html', joke= joke)
    
    else:

        #This is the value which the user gave to the previous joke which is represented by joke_num
        value = request.form["rating"]
        session.pop('rating',None)

        #get the joke_num
        last_joke = session['joke_num']
        session.pop('joke_num',None)

        prev_joke = session['prev_joke']
        session.pop('prev_joke',None)

        #RDS ADD JOKE FOR FUTURE ANALYSIS
        joke_add = Jokes(joke = prev_joke,rating = value)

        db.session.add(joke_add)
        db.session.commit()
    
    
        #now that we have the joke number we will create the svd with this information
        
        #check if session is set
        if 'user_pref' in session:

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
            new_joke_number = joke_num#needs to be the one that is being recommend_joke
            
            #set the sessions
            session['joke_num'] = new_joke_number
            session['user_pref'] = user_pref
            session['prev_joke'] = joke


            return render_template('recommended_jokes.html', joke= new_joke)

#################### FUNCTION FOR ADDING DATA TO RDS


def add_data():

    #first we add the ratings data
    rating = pd.read_csv('rating.csv')

    #loop through the ratings and create UserRatingObject and add to rds
    #commit at the end



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    debug = True
