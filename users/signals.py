import django
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

from mistakes.settings import EMAIL_HOST_USER
from .models import Profile

# @receiver(post_save, sender=Profile)


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        subject = "Welcome to the Mistakes Batallion"
        message = f"Hello {profile.name},\
        Super glad to have you here, Hope you have\
        the finest time of your life. mail me here\
        or send me  a message on mistakes if you\
        have any suggestions or issues."
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    # line prevents infinite loop, GEnIus I believe
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# @receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_delete.connect(deleteUser, sender=Profile)

post_save.connect(updateUser, sender=Profile)
