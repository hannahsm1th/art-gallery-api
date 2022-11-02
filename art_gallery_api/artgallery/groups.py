from rest_framework.response import Response
from rest_framework import status

"""
This API uses custom groups rather than the default Django ones.

This class handles the group permissions.

It takes the role of a request to an API view, and returns 401 if the user role is 
not in the given group.
"""

class GroupPermissions():
    def StaffOrManagerOnly(role, action=' perform that request'):
        if role not in ['MA', 'ST']:
            return Response({'message': 'Only staff or managers can ' + action}, status=status.HTTP_401_UNAUTHORIZED)

    def ManagerOnly(role, action=' perform that request'):
        if role not in ['MA']:
            return Response({'message': 'Only managers can ' + action}, status=status.HTTP_401_UNAUTHORIZED)
    
    def EducatorOnly(role, action=' perform that request'):
        if role not in ['ED', 'MA', 'ST']:
            return Response({'message': 'Only education users can ' + action}, status=status.HTTP_401_UNAUTHORIZED)

    def UsersOnly(role, action=' perform that request'):
        if role not in ['MA', 'ST', 'VI', 'ED']:
            return Response({'message': 'Only registered users can ' + action}, status=status.HTTP_401_UNAUTHORIZED)