from django.db import models

class Artist(models.Model):
    """
    Model class for artists.
    """
    title = models.CharField(max_length=100, blank=False)
    sort_title = models.CharField(max_length=100, blank=False)
    birth_date = models.IntegerField(blank=False)
    death_date = models.IntegerField(null = True, blank=True)
    description = models.CharField(max_length=1000, blank=True, default='')
    created_date = models.DateTimeField(auto_now_add=True, blank=False, editable=False)
    last_modified = models.DateTimeField(auto_now=True, blank=False, editable=False)

    def __str__(self):
        """ The representation that is visible in the admin """
        return self.sort_title