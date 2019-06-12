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

	def get_most_popular(self):
		popular_rated = self.data_final[self.data_final['Rating'] == 10]
		popular_jokes = popular_rated.groupby('JokeID').count().reset_index()
		popular_jokes = popular_jokes[['JokeID','Rating']]
		popular_jokes.columns = ['JokeID','Number_rated10']
		top_joke = popular_jokes.sort_values(by=['Number_rated10']).head(1)
		top_joke_val = top_joke['JokeID'].values[0]
		jokes_list = self.data_final['JokeID'].unique().tolist()
		joke_num = jokes_list.index(top_joke_val)
		top_joke_desc = self.data_jokes[self.data_jokes['JokeID'] == top_joke_val].values[0][1]

		return top_joke_desc, joke_num

	def get_interaction(self):
    
		#create interaction matrix 
		interaction_matrix =self.data_final.pivot(index = 'User_ID', columns ='JokeID', values = 'Rating').fillna(0)
		interaction_matrix =interaction_matrix.reset_index(drop=True)

		return interaction_matrix

	def append_new_user(self,interaction_df, user_pref):

		user_pref = pd.DataFrame(user_pref).T
		user_pref.columns = list(interaction_df.columns)
		user_pref.rename(index = {0:max(interaction_df.index)+1 }, 
		                                 inplace = True) 
		frames = [interaction_df, user_pref]
		new_df = pd.concat(frames)
		return new_df

	def get_svd(self,new_df):

		new_matrix = new_df.as_matrix()
		
		#get the mean score of users
		mean_score = np.mean(new_matrix,axis = 1)
		new_matrix_dm = new_matrix - mean_score.reshape(-1,1)
		#decompose interaction matrix
		U, sigma, Vt = svds(new_matrix_dm, k = 5)
		sigma = np.diag(sigma)
		all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + mean_score.reshape(-1, 1)
		preds_df = pd.DataFrame(all_user_predicted_ratings, columns = new_df.columns)


		return preds_df


	def recommend_joke(self,preds_df,already_rated):
		#already rated is a list which shows which all jokes he has rated
		#all the jokes which aren't rated will have 0s in them

		unrated_ind = []
		for i in range(len(already_rated)):

			if already_rated[i]==0:
				unrated_ind.append(i)

		#now we have all the index of jokes he has not rated

		#get the last line
		last_row = preds_df.iloc[[len(preds_df)-1]].values[0]
		best_rating = -100
		joke_num = -1

		#iterate over the last row to get the best rating
		for i in unrated_ind:

			if last_row[i] > best_rating:
				best_rating = last_row[i]
				joke_num = i

		jokes_list = self.data_final['JokeID'].unique().tolist()
		joke_index = jokes_list[joke_num]

		recommended_joke = self.data_jokes[self.data_jokes['JokeID'] == joke_index].values[0][1]

		return recommended_joke, joke_num


