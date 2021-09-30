from django.urls import path
from project.views import *

urlpatterns = [
    path('get-statistic', get_statistic, name='get_statistic'),
    path('save-statistic', save_statistic, name='save_statistic'),
    path('delete-statistic', delete_statistic, name='delete_statistic'),
]
