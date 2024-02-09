from django.core.mail import send_mail
import random
from django.conf import settings
from .models import User

def send_otp_via_email(email):
    subject = 'Otp for account verification'
    otp = random.randint(1000, 9999)
    message = f'Your Otp is {otp}'
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from, [email])
    user_obj = User.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()

def send_reset_password_email(email, link):
    subject = "Reset Password Link"
    message = "Hai, You can click the link for reset the password " + link
    email_from = settings.EMAIL_HOST
    send_mail(subject, message, email_from,[email])
