import threading
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from Event_master.settings import EMAIL_HOST_USER


class EmailThread(threading.Thread):

    def __init__(self, type, subject, html_message, receiver):
        self.subject = subject
        self.html_message = html_message
        self.receiver = receiver
        self.type = type
        threading.Thread.__init__(self)

    def send_simple_text_email(self):
        send_mail(
            self.subject,
            self.message,
            EMAIL_HOST_USER,
            [self.receiver],
            fail_silently=True
        )

    def send_html_email(self):
        text_content = ''
        msg = EmailMultiAlternatives(
            self.subject, text_content, EMAIL_HOST_USER, [self.receiver])
        msg.attach_alternative(self.html_message, "text/html")
        msg.send()

    def run(self):
        if self.type == "HTML":
            self.send_html_email()
        else:
            self.send_simple_text_email()
