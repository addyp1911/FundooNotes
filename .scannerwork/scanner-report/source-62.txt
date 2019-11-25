"""
******************************************************************************
* Purpose: purpose is to define the functions for encoding and decoding of json web token using SHORT URL
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""

from django_short_url.models import ShortURL
import jwt
from fundoonote import settings


def encode_token(username, email):
    # create jwt token, this token is in byte form therefore we decode and convert into string format
    jwt_token = jwt.encode({'user': username, 'email': email}, settings.SECRET_KEY,
                           algorithm='HS256').decode('utf-8')
    return jwt_token


def decode_token(token):
    token_obj = ShortURL.objects.get(surl=token)
    token = token_obj.lurl
    decoded = jwt.decode(token, settings.SECRET_KEY)
    return decoded
