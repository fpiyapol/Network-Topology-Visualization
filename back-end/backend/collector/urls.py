from django.urls import path

from .views import DeviceView, UpdateView

app_name = "devices"

# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('devices/', DeviceView.as_view()),
    path('devices/<int:pk>', DeviceView.as_view()),
    path('update/', UpdateView.as_view()),
]