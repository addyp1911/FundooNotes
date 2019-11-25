"""
******************************************************************************
* Purpose: purpose is to upload to and delete image from Amazon s3 bucket
*
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""

from fundoonote import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from services.utils import logger
from botocore.exceptions import ClientError
import boto3


class AmazonS3:

    def upload_file(self, file_name, object_name=None):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        # Upload the file
        s3_client = boto3.resource('s3',
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        try:
            response = s3_client.upload_file(file_name, object_name)
        except ClientError as error:
            logger.error(error)
            return False
        return response

    def delete(self, object_name):
        """delete a file to an S3 bucket
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        # If S3 object_name was not specified, use file_name
        s3_client = boto3.resource('s3',
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
        try:
            response = s3_client.delete_object(Key='image/' + object_name)
        except ClientError as error:
            logger.error(error)
            return False
        return response

