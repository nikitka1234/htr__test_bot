import boto3
from os import getenv


session = boto3.session.Session()
s3 = session.client(
    service_name='s3',
    aws_access_key_id=getenv("ACCESS_KEY"),
    aws_secret_access_key=getenv("SECRET_ACCESS_KEY"),
    endpoint_url='https://storage.yandexcloud.net'
)


async def upload_file(object_name, bucket_name, object_bucket_name):
    s3.upload_file(object_name, bucket_name, object_bucket_name)


async def delete(bucket_name, object_name):
    s3.delete_object(BUCKET=bucket_name, KEY=object_name)


async def download(bucket_name, object_name):
    s3.download_file(bucket_name, object_name, object_name)
