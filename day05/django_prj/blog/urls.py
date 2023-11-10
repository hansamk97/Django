from django.urls import path
from . import views

urlpatterns=[
    # localhost:8000/blog
    path('',views.index),
    # localhost:8000/blog/4(pk, int)
    path('<int:pk>/',views.single_post_page),
]