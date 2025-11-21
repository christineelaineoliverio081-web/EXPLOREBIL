from django import template
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def media_url(path):
    """Convert media URLs to static URLs in production"""
    if 'RENDER' in os.environ:
        # In production, media files are served as static files
        return settings.STATIC_URL + path.replace('media/', '')
    else:
        # In development, use normal media URL
        return settings.MEDIA_URL + path