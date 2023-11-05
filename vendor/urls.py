from django.urls import path
from . import views

app_name = 'vendor'
urlpatterns = [
    path('review/<slug:slug>/<uuid:id>', views.new_review, name='new_review'),
]