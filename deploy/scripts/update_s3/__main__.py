import boto3 # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from git import Repo # type: ignore
from typing import TypedDict, List
import json


load_dotenv()  # take environment variables from .env.


FOLDER_PATHS = ['./deploy/aws/cloudformation']
S3_USER_ACCESS_ID = os.getenv('S3_USER_ACCESS_ID')
S3_USER_SECRET_KEY = os.getenv('S3_USER_SECRET_KEY')
OLLI_CONFIG_BUCKET_NAME = os.getenv('OLLI_CONFIG_BUCKET_NAME')


class Version(TypedDict):
    version: str
    release_date: str


if __name__ == '__main__':
    for FOLDER_PATH in FOLDER_PATHS:
        assert isinstance(FOLDER_PATH, str) and \
            isinstance(S3_USER_ACCESS_ID, str) and \
            isinstance(S3_USER_SECRET_KEY, str) and \
            isinstance(OLLI_CONFIG_BUCKET_NAME, str)
        filepaths: List[str] = [os.path.join(FOLDER_PATH, file) for file in os.listdir(FOLDER_PATH)]
        object_names = [file.split('.')[0] for file in os.listdir(FOLDER_PATH)]
        #Creating Session With Boto3.
        session = boto3.Session(
            aws_access_key_id=S3_USER_ACCESS_ID,
            aws_secret_access_key=S3_USER_SECRET_KEY
        )
        # Creating S3 Resource From the Session.
        s3 = session.resource('s3') 
        for i, file in enumerate(filepaths):
            s3.Bucket(OLLI_CONFIG_BUCKET_NAME).upload_file(file, object_names[i], ExtraArgs={'ACL':'public-read'})
