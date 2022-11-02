from rest_framework import status
from rest_framework.parsers import FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from artgallery.groups import GroupPermissions
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse
from artists.models import Artist
from artists.serializers import ArtistSerializer

class ListArtists(APIView):
    """
    View to list all artists in the system from model: `artists.Artist`.

    * Requires basic authentication.
    * Only staff and managers are able to update or create artists.
    * Only managers can delete artists
    """

    authentication_classes = [authentication.BasicAuthentication]

    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "Tracey Moffatt",
                            "sort_title": "Moffatt, Tracey",
                            "birth_date": 1960,
                            "death_date": 'null',
                            "description": "",
                            "created_date": "2022-10-12T01:07:29.774000Z",
                            "last_modified": "2022-10-12T01:07:29.774000Z"
                        },
                        {
                            "id": 2,
                            "title": "Vincent Namatjira",
                            "sort_title": "Namatjira, Vincent",
                            "birth_date": 1983,
                            "death_date": 'null',
                            "description": "An artist",
                            "created_date": "2022-10-12T01:13:36.219000Z",
                            "last_modified": "2022-10-12T02:43:04.347000Z"
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all artists.')
        }
    )
    def get(self, request, format=None):
        """
        Return a list of all artists.
        """
        permission_classes = [permissions.AllowAny]
        artists = Artist.objects.all()
        title = request.GET.get('title', None)
        if title is not None:
            artists = artists.filter(title__icontains=title)
        artists_serializer = ArtistSerializer(artists, many=True)
        return Response(artists_serializer.data)

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful creation',
                status_codes=['201'],
                value =
                {
                    "title": "Daniel Boyd",
                    "sort_title": "Boyd, Daniel",
                    "birth_date": 1982,
                    "death_date": 'null',
                    "description": "An indigenous artist"
                },
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "sort_title": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'application/x-www-form-urlencoded': ArtistSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful creation will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data, will return bad request and details about required inputs.'),
        }
    )
    def post(self, request, format=None):
        """
        Add an artist to the list of all artists.

        * Only managers or staff can add artists
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'add new artists')
        if auth_denied is None:
            artist_data = FormParser().parse(request)
            artist_serializer = ArtistSerializer(data=artist_data)
            if artist_serializer.is_valid():
                artist_serializer.save()
                return Response(artist_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema( 
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.')
        }
    )
    def delete(self, request, format=None):
        """
        Delete all artists.

        * Only managers can do this action
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete all artists')
        if auth_denied is None:
            count = Artist.objects.all().delete()
            return Response({'message': '{} artists were deleted.'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied


class ListArtistDetail(APIView):
    """
    View to list a single artist in the system.

    * Requires basic authentication.
    * Only managers or staff can update an artist
    * Only managers can delete an artist
    """
    authentication_classes = [authentication.BasicAuthentication]

    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data for the requested artist.',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 2,
                            "title": "Vincent Namatjira",
                            "sort_title": "Namatjira, Vincent",
                            "birth_date": 1983,
                            "death_date": 'null',
                            "description": "An artist",
                            "created_date": "2022-10-12T01:13:36.219000Z",
                            "last_modified": "2022-10-12T02:43:04.347000Z"
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the requested artist.'),
            404: OpenApiResponse(response=int, description='The given id does not match any artist is in the database.'),
        }
    )
    def get(self, request, pk):
        """
        Return an artist.
        """
        permission_classes = [permissions.AllowAny]
        try:
            artist = Artist.objects.get(pk=pk)
        except Artist.DoesNotExist:
            return Response({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
        artist_serializer = ArtistSerializer(artist)
        return Response(artist_serializer.data)

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful update',
                status_codes=['201'],
                value =
                    [
                        {
                            "id": 2,
                            "title": "Vincent Namatjira",
                            "sort_title": "Namatjira, Vincent",
                            "birth_date": 1983,
                            "death_date": 'null',
                            "description": "An artist",
                            "created_date": "2022-10-12T01:13:36.219000Z",
                            "last_modified": "2022-10-12T02:43:04.347000Z"
                        }
                    ],
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "sort_title": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'application/x-www-form-urlencoded': ArtistSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful update will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data will return bad request and details about required inputs.'),
        }
    )    
    def put(self, request, pk):
        """
        Update an artist.
        * Only managers or staff can update an artist
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'update an artist')
        if auth_denied is None:
            try:
                artist = Artist.objects.get(pk=pk)
            except Artist.DoesNotExist:
                return Response({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
            artist_data = FormParser().parse(request)
            artist_serializer = ArtistSerializer(artist, data = artist_data, partial=True)
            if artist_serializer.is_valid():
                artist_serializer.save()
                return Response(artist_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(artist_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema(
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.'),
            404: OpenApiResponse(response=int, description='The given id does not match any artist is in the database.'),
        }
    )
    def delete(self, request, pk):
        """
        Delete an artist.
        * Only managers can delete an artist
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete artists')
        if auth_denied is None:
            try:
                artist = Artist.objects.get(pk=pk)
            except Artist.DoesNotExist:
                return Response({'message': 'The artist does not exist'}, status=status.HTTP_404_NOT_FOUND)
            artist.delete()
            return Response({'message': 'Artist was deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied