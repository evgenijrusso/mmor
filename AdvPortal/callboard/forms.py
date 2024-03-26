from allauth.account.forms import SignupForm
from string import hexdigits
import random
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.core.mail import send_mail


class CommonSignupForm(SignupForm):

    def save(self, request):
        # Ensure you call the parent class's save. Save() returns a User object.
        user = super(CommonSignupForm, self).save(request)
        user.is_active = False
        code = ''.join(random.sample(hexdigits, k=5))
        user.code = code
        user.save()
        send_mail(
            subject=_('Activation code'),           # Код активации
            message=_('Account activation code'),    # Код активации аккаунта
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )

        return user
