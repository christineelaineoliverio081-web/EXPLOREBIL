from django.contrib import admin
from .models import Municipality, TouristSpot, TouristSpotImage, Review, Rating

@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

class TouristSpotImageInline(admin.TabularInline):
    model = TouristSpotImage
    extra = 3
    fields = ('image', 'caption', 'display_order')

@admin.register(TouristSpot)
class TouristSpotAdmin(admin.ModelAdmin):
    list_display = ('name', 'municipality', 'address', 'created_at')
    list_filter = ('municipality', 'created_at')
    search_fields = ('name', 'description', 'address')
    date_hierarchy = 'created_at'
    inlines = [TouristSpotImageInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'municipality', 'description', 'address', 'image')
        }),
        ('Map Location', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at',),
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(TouristSpotImage)
class TouristSpotImageAdmin(admin.ModelAdmin):
    list_display = ('tourist_spot', 'caption', 'display_order')
    list_filter = ('tourist_spot',)
    search_fields = ('tourist_spot__name', 'caption')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'tourist_spot', 'comment', 'created_at')
    list_filter = ('tourist_spot', 'created_at')
    search_fields = ('user__username', 'tourist_spot__name', 'comment')
    date_hierarchy = 'created_at'
    actions = ['delete_selected']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'tourist_spot', 'rating', 'created_at')
    list_filter = ('rating', 'tourist_spot', 'created_at')
    search_fields = ('user__username', 'tourist_spot__name')
    date_hierarchy = 'created_at'
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion of ratings
