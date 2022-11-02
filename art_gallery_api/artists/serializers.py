from rest_framework import serializers
from artists.models import Artist

class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = (
            'id',
            'title',
            'sort_title',
            'birth_date',
            'death_date',
            'description',
            'created_date',
            'last_modified')
        
        read_only_fields = ['id', 'created_date', 'last_modified']