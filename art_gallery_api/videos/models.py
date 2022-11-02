from django.db import models

class Video(models.Model):
    """
    Model class for videos.
    """
    title = models.CharField(max_length=200, blank=False)
    video = models.FileField(upload_to='data/videos/', blank=False)
    thumbnail = models.ImageField(upload_to='data/videos/thumbnails/', blank=False)
    production_date = models.IntegerField(blank=False)
    place_of_origin = models.CharField(max_length=100, blank=False)
    length = models.CharField(max_length=100, blank=False)
    description = models.CharField(max_length=1000, blank=True, default='')
    is_public_domain = models.BooleanField(blank=False, default=False)
    creator = models.CharField(max_length=100, blank=False)
    subject = models.CharField(max_length=100, blank=False, default='')
    created_date = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, editable=False)
    published = models.BooleanField(blank=False,default=False)

    def __str__(self):
        """ The representation that is visible in the admin """
        return self.title