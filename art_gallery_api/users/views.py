from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import serializers
from artgallery.groups import GroupPermissions
from django.db import DatabaseError
from drf_spectacular.utils import extend_schema, OpenApiExample, inline_serializer, OpenApiResponse
from users.models import User
from users.serializers import UserSerializer, UserCreateUpdateSerializer

class ListUsers(APIView):
    """
    View to list all users in the system from model: `users.User`.

    * Requires basic authentication.
    * Only staff and managers are able to access this view.
    * Only managers can add users
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
                            "first_name": "Staff",
                            "last_name": "McStaffson",
                            "email": "mcstaffson@gallery.com",
                            "role": "ST",
                            "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$NFA1cjJkRXVVZTFWZFhNZTVqQjNMTA$QbILnel3w1j+jts+jQdkp2qhpKeMBeMM8HXmCUcwHg4",
                            "description": "",
                            "created_date": "2022-10-11T11:27:02.375000Z",
                            "last_modified": "2022-10-13T12:45:20.498000Z"
                        },
                        {
                            "id": 2,
                            "first_name": "Manager",
                            "last_name": "McManagerson",
                            "email": "mcmanagerson@gallery.com",
                            "role": "MA",
                            "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$VmJrbFZLR1AyTENsczZFNDVLWG50YQ$jjPzZBqB+ZN5UmWixEefYsZTFTWOb0wDCL8BH0BqU4I",
                            "description": "A fine manager",
                            "created_date": "2022-10-11T11:28:02.839000Z",
                            "last_modified": "2022-10-13T12:45:32.570000Z"
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the list of all users.')
        }
    )
    def get(self, request, format=None):
        """
        Return a list of all users.
        * Only staff and managers are able to access this view.
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'view users')
        if auth_denied is None:
            users = User.objects.all()
            users_serializer = UserSerializer(users, many=True)
            return Response(users_serializer.data)
        else:
            return auth_denied

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful creation',
                status_codes=['201'],
                value =
                {
                    "first_name": "Alice",
                    "last_name": "Allison",
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
                    "first_name": [
                        "This field is required."
                    ],
                    "last_name": [
                        "This field is required."
                    ],
                    "password": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'application/x-www-form-urlencoded': inline_serializer(
                name='InlineOneOffSerializerUser',
                fields={
                    'first_name': serializers.CharField(max_length=80),
                    'last_name': serializers.CharField(max_length=80),
                    'email': serializers.EmailField(),
                    'role': serializers.ChoiceField(choices=['MA', 'ST', 'ED','VI']),
                    'password': serializers.CharField(max_length=100),
                    'description': serializers.CharField(max_length=1000, default='')
                   }
            )
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful creation will return the input data with the password hashed.'),
            400: OpenApiResponse(response=int, description='Missing data, will return bad request and details about required inputs.'),
        }
    )
    def post(self, request, format=None):
        """
        Add a user to the list of all users.

        * Only managers can add users
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'add new users')
        if auth_denied is None:
            user_serializer = UserCreateUpdateSerializer(data=request.data)
            try:
                if user_serializer.is_valid():
                    user_serializer.save()
                    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except DatabaseError:
                return Response({'message': 'User with that email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied


class ListUserDetail(APIView):
    """
    View to list a single user in the system.

    * Requires basic authentication.
    * Only staff and managers are able to access this view.
    * Only managers can update a user's role
    * Only managers can delete a user
    """

    authentication_classes = [authentication.BasicAuthentication]

    @extend_schema(
        examples=[
            OpenApiExample(
                'Returned data for the requested user.',
                status_codes=['200'],
                value =
                    [
                        {
                            "id": 2,
                            "first_name": "Manager",
                            "last_name": "McManagerson",
                            "email": "mcmanagerson@gallery.com",
                            "role": "MA",
                            "password": "argon2$argon2id$v=19$m=102400,t=2,p=8$VmJrbFZLR1AyTENsczZFNDVLWG50YQ$jjPzZBqB+ZN5UmWixEefYsZTFTWOb0wDCL8BH0BqU4I",
                            "description": "A fine manager",
                            "created_date": "2022-10-11T11:28:02.839000Z",
                            "last_modified": "2022-10-13T12:45:32.570000Z"
                        }
                    ],
            )
        ],
        responses={
            200: OpenApiResponse(response=int, description='Returns the requested user.'),
            404: OpenApiResponse(response=int, description='The given id does not match any user is in the database.'),
        }
    )
    def get(self, request, pk):
        """
        Return a user.
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'view a user')
        if auth_denied is None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data)
        else:
            return auth_denied

    @extend_schema(
        examples=[
            OpenApiExample(
                'Successful update',
                status_codes=['201'],
                value =
                {
                    "first_name": "Alice",
                    "last_name": "Allison",
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
                    "first_name": [
                        "This field is required."
                    ],
                    "last_name": [
                        "This field is required."
                    ],
                    "password": [
                        "This field is required."
                    ]
                },
            )
        ],
        request={
            'application/x-www-form-urlencoded': inline_serializer(
                name='InlineOneOffSerializerUser',
                fields={
                    'first_name': serializers.CharField(max_length=80),
                    'last_name': serializers.CharField(max_length=80),
                    'email': serializers.EmailField(),
                    'role': serializers.ChoiceField(choices=['MA', 'ST', 'ED','VI']),
                    'password': serializers.CharField(max_length=100),
                    'description': serializers.CharField(max_length=1000, default='')
                   }
            )
        },
        responses={
            201: OpenApiResponse(response=int, description='Successful update will return the input data with the password hashed.'),
            400: OpenApiResponse(response=int, description='Missing data, will return bad request and details about required inputs.'),
        }
    )
    def put(self, request, pk):
        """
        Update a user.
        """
        auth_denied = GroupPermissions.StaffOrManagerOnly(request.user.role, 'update a user')
        role_auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'modify a user role')
        if auth_denied is None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            if 'role' in request.data.keys() and role_auth_denied is not None:
                return role_auth_denied
            user_serializer = UserSerializer(user, data = request.data, partial=True)
            try:
                user_serializer.is_valid()
            except DatabaseError:
                return Response({'message': 'User with that email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return auth_denied

    @extend_schema(
        responses={
            204: OpenApiResponse(response=int, description='Returns nothing on successful deletion.'),
            404: OpenApiResponse(response=int, description='The given id does not match any user is in the database.'),
        }
    )
    def delete(self, request, pk):
        """
        Delete a user.
        """
        auth_denied = GroupPermissions.ManagerOnly(request.user.role, 'delete users')
        if auth_denied is None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'message': 'The user does not exist'}, status=status.HTTP_404_NOT_FOUND)
            user.delete()
            return JsonResponse({'message': 'User was deleted.'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return auth_denied