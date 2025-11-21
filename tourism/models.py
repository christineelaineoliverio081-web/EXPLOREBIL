from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='municipalities/', null=True, blank=True)
    
    def __str__(self):
        return self.name

class TouristSpot(models.Model):
    name = models.CharField(max_length=200)
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name='tourist_spots')
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_spots/', null=True, blank=True)
    address = models.CharField(max_length=500)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / len(ratings)
        return 0

class TouristSpotImage(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tourist_spot_gallery/')
    caption = models.CharField(max_length=255, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']

    def __str__(self):
        return f"{self.tourist_spot.name} image #{self.id}"

class Review(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    image = models.ImageField(upload_to='review_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.tourist_spot.name}"

class Rating(models.Model):
    tourist_spot = models.ForeignKey(TouristSpot, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['tourist_spot', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.tourist_spot.name} - {self.rating} stars"
