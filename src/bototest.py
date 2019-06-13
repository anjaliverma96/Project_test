import boto3
import os
import logging
import logging.config


logger = logging.getLogger()
class Boto:

	def download_rating(self):


		"""This function downloads the recommendation system data from s3 to use in building the recommendation system"""

		logger.info("Starting download of ratings file")

		try:
			s3_resource = boto3.resource('s3')
			bucket = s3_resource.Bucket('jokerecommender')
			bucket.download_file('ratings.csv',"ratings.csv")

			logger.info("Finished download of ratings file")

		except Exception as e:
			logger.error("This error has been raised possibly due to the wrong S3 credentials/access privilege")
            logger.error(e)

            raise(e)

		

	def download_jokes(self):
		
		"""This function downloads the jokes from s3 to use in building the recommendation system"""

		logger.info("Starting download of jokes file")
		
		try:
			s3_resource = boto3.resource('s3')
			bucket = s3_resource.Bucket('jokerecommender')
			bucket.download_file("jokes.csv","jokes.csv")

			logger.info("Finished download of jokes file")

		except Exception as e:
			logger.error("This error has been raised possibly due to the wrong S3 credentials/access privilege")
			logger.error(e)
			raise(e)


