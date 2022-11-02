from rest_framework import serializers
from artworks.models import Artwork

class ArtworkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artwork
        fields = (
            'id',
            'title',
            'image',
            'thumbnail',
            'date_start',
            'date_end',
            'place_of_origin',
            'dimensions',
            'medium_display',
            'provenance_text',
            'is_public_domain',
            'latitude',
            'longitude',
            'department',
            'artist_id',
            'artist_title',
            'created_date',
            'last_modified',
            'on_display')

        read_only_fields = ['id', 'created_date', 'last_modified']