import secrets
from .models import User, Role
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, RoleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# @api_view(['POST'])
# def login(request):
#     """
#     Authenticate user and provide token.
#     """
#     user = authenticate(request, username=request.data['username'], password=request.data['password'])
#     if user is not None:
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     else:
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def logout(request):
#     """
#     Logout user and delete token.
#     """
#     try:
#         request.user.auth_token.delete()
#     except (AttributeError, ObjectDoesNotExist):
#         pass
#     return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def create_user(request):
    """
    Create a new user.
    While creating a user, we don't need to authenticate the user, as we assume that the user is a completely new user.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate a token key
        token_key = generate_token_key(user)
        
        response_data = {
            'user': serializer.data,
            'token': token_key
        }
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def generate_token_key(user):
    """
    Generate a unique token key for the user.
    """
    return secrets.token_hex(20)


@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    """
    Update an existing user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def disable_user(request, pk):
    """
    Disable an existing user.
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user.inactive = True
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_role(request):
    """
    Create a new role.
    """
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_role(request, pk):
    """
    Update an existing role.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(role, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_role(request, pk):
    """
    Delete an existing role.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    role.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
