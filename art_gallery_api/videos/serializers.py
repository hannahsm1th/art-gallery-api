from rest_framework import serializers
from videos.models import Video

class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = (
            'id',
            'title',
            'video',
            'thumbnail',
            'production_date',
            'place_of_origin',
            'length',
            'description',
            'is_public_domain',
            'creator',
            'subject',
            'created_date',
            'last_modified',
            'published')
        read_only_fields = ['id', 'created_date', 'last_modified']