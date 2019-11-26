"""
******************************************************************************
* Purpose: purpose is to upload to and delete image from Amazon s3 bucket
*
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
from fundoonote.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from services.utils import logger
from botocore.exceptions import ClientError
import boto3

from fundoonote.settings import AWS_STORAGE_BUCKET_NAME


def upload_file(file_name, bucket):
    """Upload a file to an S3 bucket
    :param bucket: The name of our AWS S3 bucket
    :param file_name: File to upload
    :return: True if file was uploaded, else False
    """
    # If S3 object_name was not specified, use file_name
    try:
        s3_resource = boto3.resource(service_name='s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        s3_resource.meta.client.upload_file(Filename=file_name, Bucket=bucket,
                                            Key='new_upload/{}'.format(file_name))
        s3_resource.create_bucket(Bucket='Hello4309')
        s3_resource.Object('Hello4309', file_name).upload_file(Filename=file_name)
    except ClientError as error:
        logger.error(error)
        return False


def delete_file(object_name):
    """delete a file from an S3 bucket
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    s3_client = boto3.resource('s3',
                               aws_access_key_id=AWS_ACCESS_KEY_ID,
                               aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    try:
        bucket = s3_client.Bucket(AWS_STORAGE_BUCKET_NAME)
        source_file_name = object_name
        objects_to_delete = []
        for obj in bucket.objects.filter(Prefix=source_file_name):
            objects_to_delete.append({'Key': obj.key})
        bucket.delete_objects(
            Delete={
                'Objects': objects_to_delete
            })
    except ClientError as error:
        logger.error(error)
        return False
