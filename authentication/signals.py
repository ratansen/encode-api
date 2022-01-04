from django_rest_passwordreset.tokens import BaseTokenGenerator
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import EmailMessage


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_body = """\
    <html>
      <head></head>
      <body>
        Dear <b>%s</b>,
        <p>The OTP for password reset is <b>%s</b>. The OTP is valid for 6 minutes. </p>
        <p>Regards,<br>Alcheringa Web Operations</p>
      </body>
    </html>
    """ % (reset_password_token.user.email, reset_password_token.key)

    email = EmailMessage('Reset Password for Alcheringa', email_body, to=[
                         reset_password_token.user.email])
    email.content_subtype = "html"
    email.send()
