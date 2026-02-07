from django.urls import re_path,path
from . import consumers

websocket_urlpatterns = [
    path('ws/some/', consumers.BalanceSlash.as_asgi()),
]