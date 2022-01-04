from django.urls import path, include
from bus import views



urlpatterns = [
    path('all/', views.allBusListAPI.as_view()),
    path('detail/<id>/', views.BusDetailAPI.as_view()),
    path('create/', views.BusCreateAPI.as_view()),
    path('update/<pk>/', views.BusUpdateAPI.as_view()),
]
