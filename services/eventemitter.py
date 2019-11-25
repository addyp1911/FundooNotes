"""
******************************************************************************
* Purpose: purpose is to define the event handler methods to which the activation message is sent
* @author POOJA ADHIKARI
* @version 3.7
* @since 22/10/2019
******************************************************************************
"""

from pathlib import *
from django.core.mail import EmailMessage
from dotenv import load_dotenv, find_dotenv
from pyee import BaseEventEmitter

ee = BaseEventEmitter()
load_dotenv(find_dotenv())
env_path = Path('.') / '.env'


@ee.on('event')
def email_handler(link, mail_subject, email):
    """
    :param link: This message is the activation link sent to the user for confirmation of registration
    :param mail_subject: The mail subject is "activation of  user useraccount"
    :param email: the user entered email to which activation link is sent
    :return: returns the activation status,true if message is sent successfully,false if not
    """

    my_email = EmailMessage(
        mail_subject, link, to=[email]
    )
    status = my_email.send()
    return status


@ee.on('forgot_password')
def forgot_password_handler(reset_message, mail_subject, email):
    """
    :param reset_message: This message is the activation link sent to the user for confirmation of registration
    :param mail_subject: The mail subject is "activation of  user useraccount"
    :param email: the user entered email to which activation link is sent
    :return: returns the activation status,true if message is sent successfully,false if not
    """

    my_email = EmailMessage(
        mail_subject, reset_message, to=[email]
    )
    status = my_email.send()
    return status


