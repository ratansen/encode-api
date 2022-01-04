from django.shortcuts import render
from bus.models import Bus
from rest_framework import generics, permissions, status, mixins
from rest_framework.response import Response
import django_filters.rest_framework
from rest_framework_jwt.settings import api_settings
from rest_framework import viewsets
from bus.serializers import BusSerializer
# Create your views here.

#Show list of all buses
class allBusListAPI(generics.ListAPIView):
    serializer_class = BusSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Bus.objects.all()
    ilter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_fields = ('driver', 'destination_from',
                     'destination_to', 'date_of_departure', 'date_of_arrival')
    
#Show details of a particular bus
class BusDetailAPI(generics.ListAPIView):
    serializer_class = BusSerializer
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)
    def get_queryset(self):
        queryset = Bus.objects.filter(pk=self.kwargs['id'])
        return queryset


class BusCreateAPI(generics.GenericAPIView, mixins.CreateModelMixin):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request):
        return self.create(request)


class BusUpdateAPI(generics.GenericAPIView, mixins.UpdateModelMixin):
    serializer_class = BusSerializer
    queryset = Bus.objects.all()
    permission_class = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request,pk):
        return self.update(request, pk)
