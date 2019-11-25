"""
******************************************************************************
* Purpose: purpose is to define the custom decorators in which the json web token is decoded and the access to a
protected API view
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import json
import jwt
import redis
from django.http import HttpResponse
from services.pyjwt import decode_token

redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def decorator_login(func):
    def inner(request):
        try:
            token = request.META.get('HTTP_AUTHORIZATION')
            decoded = decode_token(token)
            username = decoded['user']
            if token == redis_db.get(username).decode('utf-8'):
                return func(request)
        except(KeyError, jwt.DecodeError,
               jwt.ExpiredSignature):
            data = {'error': "Bad Request,the token has expired or incorrect token"}
            return HttpResponse(json.dumps(data))
        return inner
