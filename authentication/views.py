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

ROLE_CHOICES = (
    (1, 'bus_admin'),
    (2, 'bus_terminus_admin'),
    (3, 'passenger'),
)
class PhoneView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        phone = request.data.get("phone", "")
        fullname = request.data.get("fullname", "")
        password = request.data.get("password", "password")
        group = request.data.get("group", 3)
        if (User.objects.filter(phone=phone,role=group)):
            user = User.objects.filter(phone=phone, role=group).first()
            user.fullname = fullname
            user.save()
            user = authenticate(request, phone=phone, password=password)
            login(request, user)
        elif(User.objects.filter(phone=phone)):
            return Response(data={"success": False, "message":"Same phone number exists with different role",}, status=status.HTTP_403_FORBIDDEN)
        else:
            user=User.objects.create_user(
                password=password, fullname=fullname, phone=phone, role=group)
            user.save()
        token = jwt_encode_handler(jwt_payload_handler(user))
        serializer = UserSerializer(user, context={'request': request})
        return Response(data={"success": True, "data": serializer.data, "token": token}, status=status.HTTP_200_OK)
