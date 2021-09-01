from django.contrib import admin
from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('<str:id>', detail, name="detail"),
    path('new/', new, name="new"),
    path('edit/<str:id>', edit, name="edit"),
    path('delete/<str:id>', delete, name="delete"),
    path('gallery/', gallery, name="gallery"),
    path('search/', search, name='search'),
    path('create_comment/<str:article_id>', create_comment, name="create_comment"),
    path('create_re_comment/<int:article_id>/<str:comment_id>', create_re_comment, name="create_re_comment"),
    path('delete_comment/<int:article_id>/<int:comment_id>', delete_comment, name="delete_comment"),
]