from django.urls import path
from api import views

urlpatterns=[
    path("",views.SectorSerializer.as_view()),
    path("list-job/",views.JobSerializer.as_view())
]