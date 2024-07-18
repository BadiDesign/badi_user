from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class Email:
    @staticmethod
    def send_login_token(text, email):
        try:
            print(f'Send code for {email} - Code: {text}')
            subject = 'Forgot Password SmartBaj'
            html_content = render_to_string('email/code.html', {
                'token': text,
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            msg = EmailMultiAlternatives(subject, 'LOGIN TOKEN FOR SmartBaj.', email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print('Error in Send Email:', e)
            return False
        return True

    @staticmethod
    def send_forgot_link(text, email):
        try:
            print(f'Send code for {email} - Code: {text}')
            subject = 'Forgot Password SmartBaj'
            html_content = render_to_string('email/code.html', {
                'token': text,
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            msg = EmailMultiAlternatives(subject, 'LOGIN TOKEN FOR SmartBaj.', email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print('Error in Send Email:', e)
            return False
        return True

    @staticmethod
    def send_verify_link(text, email):
        try:
            print(f'Verify Email {email} - Code: {text}')
            subject = 'Verify Email SmartBaj'
            html_content = render_to_string('email/verify.html', {
                'token': text,
            })
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            msg = EmailMultiAlternatives(subject, 'Verify Email SmartBaj.', email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print('Error in Send Email:', e)
            return False
        return True

    @staticmethod
    def send_custom_template(template, email, attrs=None, subject=""):
        if attrs is None:
            attrs = {}
        try:
            print(f'Verify Email {email} - Template: {template}')
            subject = subject
            html_content = render_to_string(template, attrs)
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            msg = EmailMultiAlternatives(subject, subject, email_from, recipient_list)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
        except Exception as e:
            print('Error in Send Email:', e)
            return False
        return True
