import pandas as pd
import numpy as np
import sklearn
import pickle
import matplotlib.pyplot as plt
from scipy.sparse.linalg import svds
from sklearn.model_selection import train_test_split
from scipy.stats import rankdata

class Recommender:


	data_final = None
	data_joke = None
	def __init__(self, data_final, data_joke):

		self.data_final = data_final
		self.data_jokes = data_joke

	# Define function that returns the joke that will be displayed as default to all users on
	# their first visit to the page. 

	def get_most_popular(self):

		"""Finds the joke that is given a rating of 10 by maximum users.
    Args:
        None

    Returns:
        (tuple): Tuple consisting of the top rated textual joke as well as the
        index at which the joke_id for the top rated joke occurs in the unique list of joke ids
    """
		popular_rated = self.data_final[self.data_final['Rating'] == 10]
		popular_jokes = popular_rated.groupby('JokeID').count().reset_index()
		popular_jokes = popular_jokes[['JokeID','Rating']]
		popular_jokes.columns = ['JokeID','Number_rated10']
		top_joke = popular_jokes.sort_values(by=['Number_rated10'], ascending=False).head(1)
		top_joke_val = top_joke['JokeID'].values[0]
		jokes_list = sorted(set(self.data_final['JokeID']))
		joke_num = jokes_list.index(top_joke_val)
		top_joke_desc = self.data_jokes[self.data_jokes['JokeID'] == top_joke_val].values[0][1]

		return top_joke_desc, joke_num

	# Define function that transforms data to user-item interaction matrix

	def get_interaction(self):

		"""Transforms the dataframe with user ratings to a user-item interaction matrix.
    Args:
        None

    Returns:
        interaction_matrix(:py:class:`pandas.DataFrame`): Pandas dataframe with unique user records and ratings
        for each joke by the user
    """
    
		#create interaction matrix 
		interaction_matrix =self.data_final.pivot(index = 'User_ID', columns ='JokeID', values = 'Rating').fillna(0)
		interaction_matrix =interaction_matrix.reset_index(drop=True)

		return interaction_matrix

	# Define function that appends row with ratings for each joke by a new user, to existing interaction matrix

	def append_new_user(self,interaction_df, user_pref):

		"""Appends user_pref as the last row of the interaction_df.
    Args:
        interaction_df (:py:class:`pandas.DataFrame`): DataFrame with unique user records and ratings
        for each joke by the user (i.e. interaction_matrix)
        user_pref (:obj:`list`): List with ratings for jokes viewed by new user and 0s for unrated jokes
     
    Returns:
        new_df (:py:class:`pandas.DataFrame`): DataFrame with user_pref appended as the last row
    """


		user_pref = pd.DataFrame(user_pref).T
		user_pref.columns = list(interaction_df.columns)
		user_pref.rename(index = {0:max(interaction_df.index)+1 }, 
		                                 inplace = True) 
		frames = [interaction_df, user_pref]
		new_df = pd.concat(frames)
		return new_df


	# Define function that decomposes dataframe into 3 simpler matrices and 
	# gives predicted joke ratings for new user

	def get_svd(self,new_df):

		"""Gets predicted joke ratings for all users in new_df.
    Args:
        new_df (:py:class:`pandas.DataFrame`): DataFrame with ratings for each joke by a new user, 
        appended as the last row of existing interaction matrix
        
    Returns:
        preds_df (:py:class:`pandas.DataFrame`): DataFrame with predicted joke ratings for all users in new_df
    """

		new_matrix = new_df.as_matrix()
		
		#get the mean score of users
		mean_score = np.mean(new_matrix,axis = 1)
		new_matrix_dm = new_matrix - mean_score.reshape(-1,1)
		#decompose interaction matrix into U, Vt, Sigma
		U, sigma, Vt = svds(new_matrix_dm, k = 5)
		sigma = np.diag(sigma)
		all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + mean_score.reshape(-1, 1)
		preds_df = pd.DataFrame(all_user_predicted_ratings, columns = new_df.columns)
		preds_df = preds_df.round(1)

		return preds_df

	# Define function that returns recommended joke

	def recommend_joke(self,preds_df,already_rated):

		"""Recommends joke to user.
    Args:
        new_df (:py:class:`pandas.DataFrame`): DataFrame with ratings for each joke by a new user, 
        appended as the last row of existing interaction matrix
        
    Returns:
        preds_df (:py:class:`pandas.DataFrame`): DataFrame with predicted joke ratings for all users in new_df
    """
		#already rated is a list which shows which all jokes he has rated
		#all the jokes which aren't rated will have 0s in them

		unrated_ind = []
		for i in range(len(already_rated)):

			if already_rated[i]==0:
				unrated_ind.append(i)

		#now we have all the indices of jokes user has not rated

		#get the last line
		last_row = preds_df.iloc[[len(preds_df)-1]].values[0]
		best_rating = -100
		joke_num = -1

		#iterate over the last row to get the best rating
		for i in unrated_ind:

			if last_row[i] > best_rating:
				best_rating = last_row[i]
				joke_num = i

		jokes_list = sorted(set(self.data_final['JokeID']))
		#jokes_list = self.data_final['JokeID'].unique().tolist()
		joke_index = jokes_list[joke_num]

		recommended_joke = self.data_jokes[self.data_jokes['JokeID'] == joke_index].values[0][1]

		return recommended_joke, joke_num


