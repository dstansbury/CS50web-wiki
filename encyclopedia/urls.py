from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("random", views.random_page, name='random')
]
