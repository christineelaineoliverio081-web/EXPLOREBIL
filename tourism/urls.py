from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('municipalities/', views.admin_municipality_list, name='admin_municipality_list'),
    path('municipalities/add/', views.admin_municipality_add, name='admin_municipality_add'),
    path('municipalities/<int:municipality_id>/edit/', views.admin_municipality_edit, name='admin_municipality_edit'),
    path('municipalities/<int:municipality_id>/delete/', views.admin_municipality_delete, name='admin_municipality_delete'),

    path('tourist-spots/', views.admin_tourist_spot_list, name='admin_tourist_spot_list'),
    path('tourist-spots/add/', views.admin_tourist_spot_add, name='admin_tourist_spot_add'),
    path('tourist-spots/<int:spot_id>/edit/', views.admin_tourist_spot_edit, name='admin_tourist_spot_edit'),
    path('tourist-spots/<int:spot_id>/delete/', views.admin_tourist_spot_delete, name='admin_tourist_spot_delete'),
    path('tourist-spots/<int:spot_id>/map-edit/', views.admin_tourist_spot_map_edit, name='admin_tourist_spot_map_edit'),
    
    # Reviews and ratings management
    path('reviews/', views.admin_reviews_list, name='admin_reviews_list'),
    path('reviews/<int:review_id>/delete/', views.admin_review_delete, name='admin_review_delete'),
    
    # User management
    path('users/', views.admin_users_list, name='admin_users_list'),
    
    # Image management
    path('images/', views.admin_images_manage, name='admin_images_manage'),
    path('images/add/<int:spot_id>/', views.admin_add_images, name='admin_add_images'),
    path('images/delete/<int:image_id>/', views.admin_delete_image, name='admin_delete_image'),
]
