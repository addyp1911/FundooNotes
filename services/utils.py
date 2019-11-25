"""
******************************************************************************
* Purpose: purpose is to show the smd responses used throughout the project for the respective API views
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import json
import logging

from django.http import HttpResponse
from rest_framework.response import Response


def smd_response(success=False, message="the message needs to be displayed", data=[], status=""):
    return Response({'success': success, 'message': message, 'data': data}, status=status)


def http_response(success=False, message="the message needs to be displayed"):
    return HttpResponse(json.dumps({'success': success, 'message': message}))


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(lineno)d:%(pathname)s:%(message)s')
file_handler = logging.FileHandler('fundoo.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
