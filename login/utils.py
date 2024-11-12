import os
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv
load_dotenv()
class Util:
    @staticmethod
    def send_registration_email(user, confirmation_link):
        """
        Sends a verification email
        """
        subject = 'Confirm your email'
        sender = os.getenv('EMAIL_HOST_USER')
        receiver = [user.email]

        text_content = 'Thank you for registering with Videoflix. To complete your registration and verify your email address, click the link below: ' + confirmation_link
        html_content = render_to_string('registration_email.html', {'confirmation_link': confirmation_link})

        msg = EmailMultiAlternatives(subject, text_content, sender, receiver)
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def send_reset_password_email(user, confirmation_link):
        """
        Sends a password reset email
        """
        subject = 'Reset your Password'
        sender = os.getenv('EMAIL_HOST_USER')
        receiver = [user.email]

        text_content = 'Hello, /n We recently received a request to reset your password. If you made this request, please click on the following link to reset your password: ' + confirmation_link
        html_content = render_to_string('reset_password_email.html', {'confirmation_link': confirmation_link})

        msg = EmailMultiAlternatives(subject, text_content, sender, receiver)
        msg.attach_alternative(html_content, "text/html")

        msg.send()