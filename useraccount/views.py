"""
******************************************************************************
* Purpose: purpose is to define the rest API views using the django rest framework ,when
requests are passed to the handler methods (get,post)which are REST framework's Request instances
Handler methods return REST framework's Response
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""
import pdb
from smtplib import SMTPException
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django_short_url.views import get_surl
from rest_framework import permissions, status, serializers
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from services import eventemitter
from services.decorators import decorator_login
from services.redis import redis_obj
from .serializers import LoginSerializer, ForgotPasswordSerializer, RegisterSerializer
from services.utils import http_response, smd_response
from services.pyjwt import encode_token, decode_token
from .serializers import ResetPasswordSerializer


class RegisterAPIView(CreateAPIView):
    """
     An endpoint for registering the user and sending the activation link to the user entered mail via the event emitter
    """
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        """
        :param request: POST request for registering a new user
        :return: returns the 'true' response if the activation link is successfully sent to the registered mail
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        username = user_data['username']
        password = user_data['password']
        email = user_data['email']
        user = User.objects.create_user(username=username, password=password, email=email, is_active=False)
        user.save()
        mail_subject = 'Activate your user account.'
        # Get current site
        current_site = get_current_site(request)
        jwt_token = encode_token(username, password)
        token = get_surl(jwt_token).split('/s')[1]
        activation_link = 'http://' + str(current_site.domain) + reverse('email-activation',
                                                                         args=('token',)) + token + '/'
        stat = eventemitter.ee.emit('event', activation_link, mail_subject, email)
        smd = smd_response(
            success=str(stat),
            message="the user is registered successfully,the activation link is successfully sent to the user email",
            data=user_data,
            status=status.HTTP_200_OK
        )
        return smd


def activate(request, token):
    """
    :param request: POST
    :param token: activation token after the user is registered
    :return: returns an http response accordingly
    """
    try:
        print(request.user)
        decoded = decode_token(token)
        user = User.objects.get(username=decoded['user'])
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and user.is_active is False:
        user.is_active = True
        user.save()
        data = 'Thank you for your email confirmation. Now you can log into your account.'
        response = http_response(success=True,
                                 message=data
                                 )
    else:
        response = http_response(success=False,
                                 message='The user activation link maybe corrupt,user account activation not done'
                                 )
    return response


class LoginAPIView(GenericAPIView):
    """
    An endpoint for logging in the user.
    """
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        """
        :param request: POST
        :return: returns the response of authenticated user details after the user logs in
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.validated_data
            username = user_data['username']
            password = user_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                token = encode_token(username, user.email)
                user_data['authorization'] = str(token)
                redis_obj.set(username, token)
                smd = smd_response(
                    success=True,
                    message="the user is registered successfully,the activation link is successfully sent to the user email",
                    data=user_data,
                    status=status.HTTP_200_OK
                )
            else:
                smd = smd_response(
                    success=False,
                    message="the user is not registered",
                    data=user_data,
                    status=status.HTTP_400_BAD_REQUEST)

            return smd
        except User.DoesNotExist:
            raise serializers.ValidationError('Incorrect Credentials of the user')
        except SMTPException as e:
            return Response('There was an error sending an email: ', e)


class HelloView(APIView):
    """
       An endpoint for showing the hello message after the user logs in after built in drf authentication
    """
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request):
        """
        :param request: GET
        :return: returning the response enclosed in the message of the authenticated logged in user
        """
        token = request.META.get('HTTP_AUTHORIZATION')
        print(token)
        content = {'success': True, 'message': 'Hello, World!'}
        return Response(content)


class DetailsView(APIView):
    """
       An endpoint for showing the hello message after the user logs in after user defined drf token authentication
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    @decorator_login
    def get(request):
        """
        :param request: GET
        :return: returning the response enclosed in the message of the authenticated logged in user
        """
        print(request.user)
        content = {'success': True, 'message': 'Hello, World!'}
        return Response(content)


class PasswordForgotAPIView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = ForgotPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            email = user_data['email']
            username = user_data['username']
            user = User.objects.get(username=username)
            mail_subject = 'Confirmation mail,hello user,forgot password? this is your token to' \
                           ' reset your password'
            jwt_token = encode_token(user.username, email)
            token = get_surl(jwt_token).split('/s/')[1]
            reset_message = token
            eventemitter.ee.emit('forgot_password', reset_message, mail_subject, email)
            smd = smd_response(
                success=True,
                message="The forgot password mail has been sent successfully to your mail",
                data=user_data,
                status=status.HTTP_200_OK)
            return smd

        except User.DoesNotExist:
            return Response({'error': 'The user is not registered with the respective credentials'})
        except SMTPException as e:
            print('There was an error sending an email: ', e)


class PasswordResetAPIView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, token, *args, **kwargs):

        try:
            serializer = ResetPasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_data = serializer.data
            new_password = user_data['new_password']
            decoded_token = decode_token(token)
            user = User.objects.get(username=decoded_token['user'])
            user.set_password(new_password)
            user.save()
            smd = smd_response(
                success=True,
                message="The password has been successfully reset",
                data=user_data,
                status=status.HTTP_200_OK)
            return smd

        except User.DoesNotExist:
            return Response({'error': 'The user is not registered with the respective credentials'})
