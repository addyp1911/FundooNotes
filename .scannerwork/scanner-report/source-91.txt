"""
Description:
This describes the serializers which are very similar to a Django Form class, and
includes similar validation flags on the various fields, such as required, max_length and default.
Serializers allow complex data such as querysets and model instances to be converted to native Python
datatypes that can then be easily rendered into JSON, XML or other content types.

Author: Pooja Adhikari
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator


class LoginSerializer(serializers.ModelSerializer):
    """
 Serializer class for user login
 """
    username = serializers.CharField()
    password = serializers.CharField(max_length=8)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class RegisterSerializer(serializers.ModelSerializer):
    """
 Serializer for creating a new registered user
 """
    email = serializers.EmailField(label='Email Address', validators=[UniqueValidator(queryset=User.objects.all())])
    confirm_email = serializers.EmailField(label='Confirm Email')
    password = serializers.CharField(label='password', max_length=10)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'confirm_email',

        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                        }

    def validate_email(self, value):
        """
     :param value: holds the email of the user for email matching
     :return: returns the value
     """
        data = self.get_initial()
        email = data.get("confirm_email")
        confirm_email = value
        if confirm_email != email:
            raise ValidationError("emails dont match")
        return value

    def validate_confirm_email(self, value):
        """
     :param value: holds the email of the user for email matching
     :return: returns the value
     """
        data = self.get_initial()
        email = data.get("email")
        confirm_email = value
        if confirm_email != email:
            raise ValidationError("emails dont match")
        return value

    def validate(self, data):
        """
     :param data:data is the ordered dictionary having the username, password and email post fields of the new user
     :return: returns the data or the validation error if the user doesn't exist
     """
        username = data['username']
        user = User.objects.filter(username=username)
        if user.exists():
            return ValidationError("this user is already registered with that username")
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    """
     Serializer for forgot password view of a particular registered user
     """
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """
     Serializer for reset password view of a particular registered user
     """

    new_password = serializers.CharField(required=True)
