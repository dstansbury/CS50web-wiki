from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("random", views.random_page, name='random'),
    path("search", views.search, name='search'),
    path("create", views.create, name="create"),
    path("wiki/<str:entry>/edit", views.edit, name='edit'),
    path("wiki/<str:enty>/save", views.save, name='save')
]
