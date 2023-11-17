from django.urls import path
from . import views

urlpatterns=[
    # localhost:8000/
    path('',views.landing),
    path('about_me/',views.about_me),
]