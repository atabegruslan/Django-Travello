from django.urls import path
from frontend.api.views import (api_index, api_dest, api_update, api_delete, api_create)

app_name = 'travello'

urlpatterns = [
    path('/', api_index, name='index'),
    path('/<id>/', api_dest, name='dest'),
    path('/<id>/update', api_update, name='update'),
    path('/<id>/delete', api_delete, name='delete'),
    path('/create', api_create, name='create'),
]
