import json
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import filters
from django.contrib.auth import authenticate, get_user_model, login
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from authentication.models import NewUser
from .serializers import TokenSerializer, UserSerializer
from django.contrib.auth.models import Group
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
User = get_user_model()


class LoginView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = UserSerializer(user, context={'request': request})
            token = jwt_encode_handler(jwt_payload_handler(user))
            return Response(data={"success": True, "token": token, "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid email or password", "success": False}, status=status.HTTP_400_BAD_REQUEST)


class RegisterUsersView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        group_name = request.data.get("group", "passenger")
        user = User.objects.filter(email=email)
        if not email and not password:
            return Response(
                data={"message": "Email and Password is required to register a user", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            return Response(
                data={"message": "User with same email address already exists", "success": False}, status=status.HTTP_400_BAD_REQUEST)
        new_user = User.objects.create_user(password=password, email=email)
        user_group = Group.objects.get(name=group_name)
        user_group.user_set.add(new_user)
        return Response(
            data={"success": True},
            status=status.HTTP_200_OK
        )


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    serializer_class = UserSerializer

    def get(self, request):
        try:
            serializer = UserSerializer(
                request.user, context={'request': request})
            status = status.HTTP_200_OK
            response = {
                'success': True,
                'detail': 'User profile fetched successfully',
                'data': serializer.data
            }

        except Exception as e:
            status = status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'detail': str(e)
            }
        return Response(response, status=status)

    def put(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=self.request.user.id)
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            user.fullname = body["fullname"]
            user.email = body["email"]
            user.phone = body["phone"]
            user.save()
            status = status.HTTP_200_OK
            response = {
                'success': True
            }

        except Exception as e:
            status= status.HTTP_400_BAD_REQUEST
            response = {
                'success': False,
                'detail': str(e)
            }
        return Response(response, status=status)
