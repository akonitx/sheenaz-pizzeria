from django.contrib.auth import user_logged_in, user_logged_out
from django.contrib.auth.models import User
from django.dispatch import receiver


from Lime.settings import mainlog


@receiver(user_logged_in, sender=User)
def add_session(request, user, **kwargs):
    """
    Add session to customer field
    """

    try:
        customer = user.customer
        customer.session = request.session.session_key
        mainlog.debug(
            f"{user.username} has loged in and set {request.session.session_key}"
        )
        customer.save()
    except User.customer.RelatedObjectDoesNotExist:
        mainlog.warning(f"{user.username} hasn't relations with Customer instance")


@receiver(user_logged_out, sender=User)
def remove_session(request, user, **kwargs):
    """
    Remove session from Customer Field
    """

    try:
        customer = user.customer
        customer.session = None
        mainlog.debug(
            f"{user.username} has loged out and removed {request.session.session_key}",
        )
        customer.save()
    except User.customer.RelatedObjectDoesNotExist:
        mainlog.warning(f"{user.username} hasn't relations with Customer instance")
