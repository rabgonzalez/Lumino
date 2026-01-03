from django_rq import job
from django.core.mail import EmailMessage

@job
def deliver_certificate(base_url, student):
    email = EmailMessage(
        subject='Email test',
        body='<h3>Hello there!</h3> <p>This is the email body</p>',
        to=[student.email],
    )
    email.content_subtype = 'html'
    email.send()