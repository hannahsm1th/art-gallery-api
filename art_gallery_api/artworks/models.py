from django.db import models

class Artwork(models.Model):
    """
    Model class for artworks.
    """
    title = models.CharField(max_length=200, blank=False)
    image = models.ImageField(upload_to='data/images/', blank=False)
    thumbnail = models.ImageField(upload_to='data/thumbnails/', blank=False)
    date_start = models.IntegerField(blank=False)
    date_end = models.IntegerField(null = True, blank=True)
    place_of_origin = models.CharField(max_length=100, blank=False)
    dimensions = models.CharField(max_length=100, blank=False)
    medium_display = models.CharField(max_length=100, blank=False)
    provenance_text = models.CharField(max_length=3000, blank=True, default='')
    is_public_domain = models.BooleanField(blank=False, default=False)
    latitude = models.FloatField(blank=False)
    longitude = models.FloatField(blank=False)
    department = models.CharField(max_length=80, blank=False)
    artist_id = models.IntegerField(blank=False)
    artist_title = models.CharField(max_length=200, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, editable=False)
    on_display = models.BooleanField(blank=False,default=False)

    def __str__(self):
        """ The representation that is visible in the admin """
        return self.title