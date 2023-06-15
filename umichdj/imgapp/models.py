from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.conf import settings
from taggit.managers import TaggableManager


class Ad(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Title must be greater than 2 characters")] )
    text = models.TextField(max_length=2500, validators=[MaxLengthValidator(2500, "No more than 2500 characters")])

    # https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True)

    picture = models.BinaryField(null=True, blank=True, editable=True)      # Picture
    content_type = models.CharField(max_length=256, null=True, blank=True, help_text='The MIMEType of the file')   # Check other MIMETypes

    # Comment
    comments = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Comment', related_name='comments_owned')
    # Favorite
    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Fav', related_name='favorite_ads')
    # # Blogs 
    # blogs = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Blog', related_name='blog_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Comment(models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)                                  
    text = models.TextField(validators=[MinLengthValidator(3, "Comment must be greater than 3 characters")] )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if len(self.text) < 100 : 
            return self.text
        return self.text[:100] + ' ...'



class Fav(models.Model) :
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # https://docs.djangoproject.com/en/4.0/ref/models/options/#unique-together
    class Meta:
        unique_together = ('ad', 'user')                                          # <<--  bear in mind it may be deprecated in new versions

    def __str__(self) :
        return '%s likes %s'%(self.user.username, self.ad.title[:15])


class Blog(models.Model) :
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Title must be greater than 2 characters")] )
    text = models.TextField(max_length=2500, validators=[MaxLengthValidator(2500, "No more than 2500 characters")], default="Sons of blues,..")
    
    # https://django-taggit.readthedocs.io/en/latest/api.html#TaggableManager
    tags = TaggableManager(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Shows up in the admin list
    def __str__(self):
        return self.title 
