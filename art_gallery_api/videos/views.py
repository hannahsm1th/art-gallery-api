from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from artgallery.groups import GroupPermissions
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse
from videos.models import Video
from videos.serializers import VideoSerializer


class ListVideos(APIView):
    """
    View to list all videos in the system from model: `videos.Videos`.

    * Requires basic authentication
    * Only staff and managers are able to view all, update or create videos.
    * Only managers can delete videos
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
                            "title": "\"Artist statement\"",
                            "video": "/data/videos/video1.mov",
                            "thumbnail": "/data/videos/thumbnails/video1thumb.png",
                            "production_date": 2021,
                            "place_of_origin": "Sydney",
                            "length": "5min 45sec",
                            "description": "",
                            "is_public_domain": False,
                            "creator": "Staff McStaffson",
                            "subject": "Artist McArtson",
                            "created_date": "2022-10-12T04:08:56.603000Z",
                            "last_modified": "2022-10-12T04:08:56.603000Z",
                            "published": False
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all videos.')
        }
    )
    def get(self, request, format=None):
        """
        Return a list of all videos.
        * Only gallery staff are able to access this view.
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'view all videos')
        if auth_denied is None:
            videos = Video.objects.all()
            title = request.GET.get('title', None)
            if title is not None:
                videos = videos.filter(title__icontains=title)
            videos_serializer = VideoSerializer(videos, many=True)
            return Response(videos_serializer.data)
        else:
            return auth_denied

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful creation',
                status_codes=['201'],
                value =
                {
                    "firstName": "Alice",
                    "lastName": "Allison",
                    "email": "alice_rules@yafoo.com",
                    "role": "VI",
                    "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$Uml0MVRIMnp2aXlPVXZCNzNRaFNKZA$6UOCflxCCsxFLwJtPYT4P45YmiTLpJcKXbCbuujjF24",
                    "description": ""
                },
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "firstName": [
                        "This field is required."
                    ],
                    "lastName": [
                        "This field is required."
                    ],
                    "password": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
             'multipart/form-data': VideoSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful creation will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data, will return bad request and details about required inputs.'),
        }
    )
    def post(self, request, format=None):
        """
        Add a video to the list of all videos.

        * Only managers or staff can add videos
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'add new videos')
        if auth_denied is None:
            video_serializer = VideoSerializer(data=request.data)
            if video_serializer.is_valid():
                video_serializer.save()
                return Response(video_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema( 
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.')
        }
    )
    def delete(self, request, format=None):
        """
        Delete all videos.

        * Only managers can do this action
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete all videos')
        if auth_denied is None:
            count = Video.objects.all().delete()
            return Response({'message': '{} videos were deleted.'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied


class ListVideoDetail(APIView):
    """
    View to list a single video in the system.

    * Requires basic authentication.
    * Only education users can view videos
    * Only managers or staff can update a video
    * Only managers can delete a video
    """
    
    authentication_classes = [authentication.BasicAuthentication]
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data for the requested video.',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "\"Artist statement\"",
                            "video": "/data/videos/video1.mov",
                            "thumbnail": "/data/videos/thumbnails/video1thumb.png",
                            "production_date": 2021,
                            "place_of_origin": "Sydney",
                            "length": "5min 45sec",
                            "description": "",
                            "is_public_domain": False,
                            "creator": "Staff McStaffson",
                            "subject": "Artist McArtson",
                            "created_date": "2022-10-12T04:08:56.603000Z",
                            "last_modified": "2022-10-12T04:08:56.603000Z",
                            "published": False
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the requested video.'),
            404: OpenApiResponse(response=int, description='The given id does not match any video is in the database.'),
        }
    )
    def get(self, request, pk):
        """
        Return a video.
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'view all videos')
        if auth_denied is None:
            try:
                video = Video.objects.get(pk=pk)
            except Video.DoesNotExist:
                return Response({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)
            video_serializer = VideoSerializer(video)
            return Response(video_serializer.data)
        else:
            return auth_denied
    
    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful update',
                status_codes=['201'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "\"Artist statement\"",
                            "video": "/data/videos/video1.mov",
                            "thumbnail": "/data/videos/thumbnails/video1thumb.png",
                            "production_date": 2021,
                            "place_of_origin": "Sydney",
                            "length": "5min 45sec",
                            "description": "",
                            "is_public_domain": False,
                            "creator": "Staff McStaffson",
                            "subject": "Artist McArtson",
                            "created_date": "2022-10-12T04:08:56.603000Z",
                            "last_modified": "2022-10-12T04:08:56.603000Z",
                            "published": False
                        }
                    ],
            ),
            OpenApiExample(
                'Missing data in the request',
                status_codes=['400'],
                value =
                {
                    "title": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'multipart/form-data': VideoSerializer
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful update will return the input data.'),
            400: OpenApiResponse(response=int, description='Missing data will return bad request and details about required inputs.'),
        }
    ) 
    def put(self, request, pk):
        """
        Update a video.
        * Only managers or staff can update a video
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'update a video')
        if auth_denied is None:
            try:
                video = Video.objects.get(pk=pk)
            except Video.DoesNotExist:
                return Response({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)
            video_serializer = VideoSerializer(video, data = request.data, partial=True)
            if video_serializer.is_valid():
                video_serializer.save()
                return Response(video_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(video_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema(
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.'),
            404: OpenApiResponse(response=int, description='The given id does not match any video is in the database.'),
        }
    )
    def delete(self, request, pk):
        """
        Delete a video.
        * Only managers can delete a video
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete videos')
        if auth_denied is None:
            try:
                video = Video.objects.get(pk=pk)
            except Video.DoesNotExist:
                return Response({'message': 'The video does not exist'}, status=status.HTTP_404_NOT_FOUND)
            video.delete()
            return Response({'message': 'Video was deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied


class ListPublishedVideos(APIView):
    """
    View to list the videos that are currrently published.

    * Only educators and gallery staff can access this view
    """

    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 1,
                            "title": "\"Artist statement\"",
                            "video": "/data/videos/video1.mov",
                            "thumbnail": "/data/videos/thumbnails/video1thumb.png",
                            "production_date": 2021,
                            "place_of_origin": "Sydney",
                            "length": "5min 45sec",
                            "description": "",
                            "is_public_domain": False,
                            "creator": "Staff McStaffson",
                            "subject": "Artist McArtson",
                            "created_date": "2022-10-12T04:08:56.603000Z",
                            "last_modified": "2022-10-12T04:08:56.603000Z",
                            "published": True
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all published videos.')
        }
    )       
    def get(self, request, format=None):
        auth_denied = GroupPermissions.EducatorOnly(request.user.role, 'view published videos')
        if auth_denied is None:
            try:
                videos = Video.objects.filter(published__in=[True]) #workaround for bug in Django querysets for booleans
            except:
                return Response({'message': 'No videos are published'}, status=status.HTTP_404_NOT_FOUND)
            video_serializer = VideoSerializer(videos, many=True)
            return Response(video_serializer.data)
        else:
            return auth_denied