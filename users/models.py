from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.deletion import SET_NULL
# Create your models here.
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(
        max_length=400, unique=True, null=True, blank=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, default="Earth, Milky Way")
    short_intro = models.CharField(
        max_length=300, default="BTW, I never wrote an intro BD")
    bio = models.TextField(blank=True, null=True)
    # profile_image = models.ImageField(
    # null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    profile_image = CloudinaryField('image', default='default.jpg')

    social_instagram = models.CharField(max_length=200, null=True, blank=True)
    social_facebook = models.CharField(max_length=200, null=True, blank=True)
    social_twitter = models.CharField(max_length=200, null=True, blank=True)
    social_linkedin = models.CharField(max_length=200, null=True, blank=True)
    social_youtube = models.CharField(max_length=200, null=True, blank=True)
    social_website = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        ordering = ['-created']

    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            self.profile_image = 'default.jpg'
            url = self.profile_image.url
        return url


class Interests(models.Model):
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4,
                          primary_key=True, unique=True, editable=False)

    def __str__(self):
        return str(self.name)


class Message(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=SET_NULL, null=True, blank=True)
    # This has related_name as in not mess up the connection,
    # also no need to do mesasage_set now, only profile.message.all
    recipient = models.ForeignKey(
        Profile, on_delete=SET_NULL, null=True, blank=True, related_name="messages")
    name = models.CharField(max_length=200, default="")
    email = models.EmailField(max_length=200, null=True, blank=True)
    subject = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField()
    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['is_read', '-created']
