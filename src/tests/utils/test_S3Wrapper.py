import boto3
from moto import mock_s3

from made.utils.S3Wrapper import S3Wrapper


@mock_s3
def test_list_folders():
    conn = boto3.resource('s3', region_name='us-east-1')
    # We need to create the bucket since this is all in Moto's 'virtual' AWS account
    conn.create_bucket(Bucket='mybucket')

    model_instance = S3Wrapper(bucket_name='mybucket', profile_name='')
    folders = model_instance.listFolders('projects/ds_004/')
    print(folders)

    # body = conn.Object('mybucket', 'steve').get()['Body'].read().decode("utf-8")

    # check the right value was returned
    # assert body == b'is awesome'
