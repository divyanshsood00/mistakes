from enum import unique
from django.db import models
import uuid
# Create your models here.
from users.models import Profile
# Inheriting models.Model for obvious reasons
from cloudinary.models import CloudinaryField


class Blog(models.Model):
    # max_length cumpulsory
    author = models.ForeignKey(
        Profile, null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    short_intro = models.CharField(max_length=300, null=True, blank=True)
    # null = True means can be null(DB knows), blank = True Can submit form with this being empty
    description = models.TextField(default=None)
    # featured_image = models.ImageField(
    #     null=True, blank=True, default='default.jpg')
    featured_image = CloudinaryField('image', default='default.jpg')
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    # Could have done (Tag) if class Tag was above, "..." delays execution so it works anyways then
    tags = models.ManyToManyField('Tag', blank=True)  # ***IMPORTANT***
    vote_total = models.IntegerField(
        default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(
        default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    # Django creates id like 1,2,3,4,5 .....
    # for id primary_key = True is compulsory
    # UUID is 16 char unique string
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['vote_ratio', '-vote_total', '-created']

    # decorator helps it running as an attribute rather than an function
    # This is genius, All I am doing is blog.getVoteCount, somewhere
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value="up").count()
        totalVotes = reviews.count()

        ratio = int((upVotes/totalVotes) * 100)
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('author__id', flat=True)
        print(queryset)
        return queryset

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            self.featured_image = 'default.jpg'
            url = self.featured_image.url
        return url


class Review(models.Model):
    # ISKO RAAT LOO BHAIJAAN
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True)
    # cascade deletes it on deleting project, SET_NULL can also be used but it doesn't delete
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE)  # ***IMPORTANT***
    body = models.TextField(null=True, blank=True)
    # raataaa maar
    value = models.CharField(max_length=200, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)

    class Meta:
        unique_together = [['author', 'blog']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, editable=False,
                          unique=True, primary_key=True)

    def __str__(self):
        return self.name
