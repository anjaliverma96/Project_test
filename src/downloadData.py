import boto3

def load_data(args):

	"""Copies data that has already been downloaded into the 'jokerecommender' S3 bucket to a bucket of the user's choice .
    Bucket name can be passed as an argument or updated in the config file.
    Args:
        args (bucketname): Includes name of s3 bucket to copy data files to
    Returns:
        None
    """

    s3 = boto3.resource('s3')

    bucketname = args.bucket

    copy_source1 = {'Bucket': 'jokerecommender', 'Key': 'ratings.csv'}
    copy_source2 = {'Bucket': 'jokerecommender', 'Key': 'jokes.csv'}

    bucket = s3.Bucket('bucketname')
    logger.info('Created bucket %s', bucketname)

    bucket.copy(copy_source1, 'ratings.csv')
    bucket.copy(copy_source2, 'jokes.csv')

    logger.info('File copied to s3 bucket %s', bucketname)
