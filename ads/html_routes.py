from django.urls import path

from . import views_html


urlpatterns = [
    path('', views_html.ad_list, name='ad_list'),
    path('ad/create/', views_html.ad_create, name='ad_create'),
    path('ad/<int:pk>/edit/', views_html.ad_edit, name='ad_edit'),
    path('ad/<int:pk>/delete/', views_html.ad_delete, name='ad_delete'),
    path('register/', views_html.register, name='register'),
    path('ad/<int:ad_id>/propose/', views_html.propose_exchange, name='propose_exchange'),
    path('proposals/public/', views_html.public_proposals_page, name='proposals_public'),
    path('proposals/my/', views_html.my_proposals_page, name='proposals_private'),
]
