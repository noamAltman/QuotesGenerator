from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('output/<quote>', views.output_quote, name='output'),
]