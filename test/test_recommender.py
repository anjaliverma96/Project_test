
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, '../src')
from recommender import Recommender

def test_get_most_popular():


	input_ratings_df = pd.DataFrame({'User_ID': [1,1,2,3,4,4,5,6,7],
		'JokeID': [7,19,8,13,15,19,15,19,19],
		'Rating':[3,10,6,9,10,10,1,10,10]})

	input_jokes_df = pd.DataFrame({'JokeID': [7,8,13,15,19],
		'Joke': ["How many feminists does it take to screw in a light bulb? That's not funny.",
		"Q. Did you hear about the dyslexic devil worshiper? A. He sold his soul to Santa.",
		'They asked the Japanese visitor if they have elections in his country. "Every morning," he answers.',
		"Q: What did the blind person say when given some matzah? A: Who the hell wrote this?",
		'Q: If a person who speaks three languages is called "trilingual," and a person who speaks two languages is called "bilingual," what do you call a person who only speaks one language? A: American!']})

	true_result = ('Q: If a person who speaks three languages is called "trilingual," and a person who speaks two languages is called "bilingual," what do you call a person who only speaks one language? A: American!', 4)

	rec = Recommender(input_ratings_df,input_jokes_df)

	test_result = rec.get_most_popular()

	assert test_result == true_result


def test_get_interaction():

	input_dict = {7: [3.0,0.0,0.0,0.0,0.0,0.0,0.0],
	8: [0.0,6.0,0.0,0.0,0.0,0.0,0.0], 13: [0.0,0.0,9.0,0.0,0.0,0.0,0.0],
	15: [0.0,0.0,0.0,10.0,1.0,0.0,0.0], 19: [10.0,0.0,0.0,10.0,0.0,10.0,10.0]}

	true_df = pd.DataFrame(input_dict)
	true_df.columns.names = ['JokeID']

	input_ratings_df = pd.DataFrame({'User_ID': [1,1,2,3,4,4,5,6,7],
		'JokeID': [7,19,8,13,15,19,15,19,19],
		'Rating':[3,10,6,9,10,10,1,10,10]})
	rec = Recommender(input_ratings_df,None)
	test_df = rec.get_interaction()

	assert test_df.equals(true_df)

def test_append_new_user():

	input_dict = {7: [3.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0],
	8: [0.0,6.0,0.0,0.0,0.0,0.0,0.0,4.0], 13: [0.0,0.0,9.0,0.0,0.0,0.0,0.0,6.0],
	15: [0.0,0.0,0.0,10.0,1.0,0.0,0.0,8.0], 19: [10.0,0.0,0.0,10.0,0.0,10.0,10.0,10.0]}

	true_df = pd.DataFrame(input_dict)
	true_df.columns.names = ['JokeID']

	input_ratings_df = pd.DataFrame({'User_ID': [1,1,2,3,4,4,5,6,7],
		'JokeID': [7,19,8,13,15,19,15,19,19],
		'Rating':[3,10,6,9,10,10,1,10,10]})

	interaction_matrix =input_ratings_df.pivot(index = 'User_ID', columns ='JokeID', values = 'Rating').fillna(0)
	interaction_matrix =interaction_matrix.reset_index(drop=True)

	input_user_pref = [2,4,6,8,10]

	rec = Recommender(input_ratings_df,None)
	test_df = rec.append_new_user(interaction_matrix,input_user_pref)

	assert test_df.equals(true_df)

def test_get_svd():

	input_dict = {7: [3.0,-0.0,0.0,-0.0,-0.0,-0.0,-0.0,0.0],8: [0.0,6.0,-0.0,0.0,-0.0,0.0,0.0,0.0],
	13: [0.0,-0.0,9.0,-0.0,-0.0,0.0,0.0,0.0], 15: [0.0,-0.0,-0.0,10.0,1.0,0.0,0.0,0.0],
	17: [-0.0,-0.0,0.0,-0.0,0.0,-0.0,-0.0,5.0], 19: [10.0,0.0,0.0,10.0,-0.0,10.0,10.0,-0.0]}

	true_df = pd.DataFrame(input_dict)
	true_df.columns.names = ['JokeID']

	input_ratings_df = pd.DataFrame({'User_ID': [1,1,2,3,4,4,5,6,7,8],
		'JokeID': [7,19,8,13,15,19,15,19,19,17],
		'Rating':[3,10,6,9,10,10,1,10,10,5]})

	interaction_matrix =input_ratings_df.pivot(index = 'User_ID', columns ='JokeID', values = 'Rating').fillna(0)
	interaction_matrix =interaction_matrix.reset_index(drop=True)

	rec = Recommender(input_ratings_df,None)
	test_df = rec.get_svd(interaction_matrix)

	assert test_df.equals(true_df)

def test_recommend_joke():

	input_dict = {7: [1.0,2.0,3.0,4.0,5.0,6.0,7.0,10.0],8: [1.0,3.0,5.0,7.0,9.0,2.0,4.0,9.0], 13: [0.0,-0.0,9.0,-0.0,-0.0,0.0,0.0,8.0],15: [0.0,-0.0,-0.0,10.0,1.0,0.0,0.0,7.0], 17: [-0.0,-0.0,0.0,-0.0,0.0,-0.0,-0.0,6.0], 19: [10.0,0.0,0.0,10.0,-0.0,10.0,10.0,5.0]}
	input_df = pd.DataFrame(input_dict)
	input_df.columns.names = ['JokeID']

	already_rated = [10,9,8,0,0,0]

	input_ratings_df = pd.DataFrame({'User_ID': [1,1,2,3,4,4,5,6,7,8],
		'JokeID': [7,19,8,13,15,19,15,19,19,16],
		'Rating':[3,10,6,9,10,10,1,10,10,9]})

	input_jokes_df = pd.DataFrame({'JokeID': [7,8,13,15, 16, 19],
		'Joke': ["How many feminists does it take to screw in a light bulb? That's not funny.",
		"Q. Did you hear about the dyslexic devil worshiper? A. He sold his soul to Santa.",
		'They asked the Japanese visitor if they have elections in his country. "Every morning," he answers.',
		"Q: What did the blind person say when given some matzah? A: Who the hell wrote this?",
		"Q. What is orange and sounds like a parrot? A. A carrot.",
		'Q: If a person who speaks three languages is called "trilingual," and a person who speaks two languages is called "bilingual," what do you call a person who only speaks one language? A: American!']})

	true_result = ("Q: What did the blind person say when given some matzah? A: Who the hell wrote this?", 3)

	rec = Recommender(input_ratings_df,input_jokes_df)

	test_result = rec.recommend_joke(input_df, already_rated)

	assert test_result == true_result





