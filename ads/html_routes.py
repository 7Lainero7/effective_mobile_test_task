from django.urls import path

from . import views_html


urlpatterns = [
    path('', views_html.ad_list, name='ad_list'),
    path('ad/create/', views_html.ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', views_html.ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', views_html.ad_delete, name='ad_delete'),
]
