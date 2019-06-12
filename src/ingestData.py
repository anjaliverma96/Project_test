import boto3 

s3 = boto3.resource("s3")
s3.create_bucket(
    Bucket='jokerecommender',
    CreateBucketConfiguration={'LocationConstraint': "us-west-2"})

s3 = boto3.client("s3")
s3.upload_file('Project/data/ratings.csv', "jokerecommender", "ratings.csv")
s3.upload_file('Project/data/jokes.csv', "jokerecommender", "jokes.csv")