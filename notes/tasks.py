from datetime import timedelta
from smtplib import SMTPException
from django.contrib.auth.models import User
from django.core import mail
from django.template.loader import render_to_string
from django.utils import timezone
from fundoonote.celery import app
from .models import Note
from services.utils import logger


@app.task(bind=True, default_retry_delay=60, max_retries=20)
def send_welcome_email_task(self, user_id, note_title, note_content):
    try:
        subject = "Mail from Google Keep"
        text = "You have set a reminder for your note at this time"
        from_email = "lilysingh365@gmail.com"
        to_email = "addyp1911@gmail.com"
        html_content = render_to_string('ReminderAlert.html',
                                        {'username': User.objects.get(id=user_id).username, 'title': note_title,
                                         'content': note_content})
        msg = mail.EmailMultiAlternatives(subject, text, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        logger.info("Sent feedback email")
        print("your mail has been successfully sent with status code" + str(msg))
    except SMTPException as e:
        raise self.retry(exc=e)


@app.task(name="checkreminders", bind=True, default_retry_delay=60, max_retries=120)
def check_reminders_task(self):
    notes_data = Note.objects.filter(reminder__isnull=False)
    reminders = notes_data.values('reminder')
    reminder_list = []
    count = 0
    for reminder in enumerate(reminders):
        reminder_list.append(reminder[1]['reminder'])
    for reminder in reminder_list:
        now = timezone.now()
        time_diff = reminder - now
        print("The reminder notes check must happen every 10 seconds")
        if timedelta(seconds=10) < time_diff <= timedelta(seconds=15):
            note = Note.objects.get(reminder=reminder)
            send_welcome_email_task.delay(note.user_id, note.title, note.content)
        count += 1


app.conf.beat_schedule = {
    'check reminders every 10 seconds': {
        'task': 'checkreminders',
        'schedule': 10.0,
    },
}
