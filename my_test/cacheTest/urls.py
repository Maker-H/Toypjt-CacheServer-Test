from django.urls import path, include
from .views import VanilaLoadTest
from .views import RedisLoadTest


urlpatterns = [
    path('test/', VanilaLoadTest),
    path('redis/', RedisLoadTest),

]
