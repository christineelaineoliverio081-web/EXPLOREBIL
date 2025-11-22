from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from tourism import views
import os

urlpatterns = [
    # Main site pages
    path('', views.welcome_view, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('municipality/<int:municipality_id>/', views.municipality_detail, name='municipality_detail'),
    path('tourist-spot/<int:spot_id>/', views.tourist_spot_detail, name='tourist_spot_detail'),
    path('search/', views.search_results, name='search_results'),
    
    # Logo and Ads Corner pages
    path('logo/', views.logo_page, name='logo_page'),
    path('poster/', views.poster_page, name='poster_page'),
    path('advertisement/', views.advertisement_page, name='advertisement_page'),
    
    # Admin dashboard
    path('admin-dashboard/', include('tourism.urls')),
    
    # Django admin
    path('django-admin/', admin.site.urls),
    
    # Google verification
    path('google18d2f562bfaf95b9.html', lambda r: HttpResponse('google-site-verification: google18d2f562bfaf95b9.html', content_type='text/html')),
    
    # SEO files
    path('sitemap.xml', lambda r: HttpResponse(open('sitemap.xml').read(), content_type='application/xml')),
    path('robots.txt', lambda r: HttpResponse(open('robots.txt').read(), content_type='text/plain')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
