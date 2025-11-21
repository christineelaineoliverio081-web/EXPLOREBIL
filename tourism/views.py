from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.utils.text import slugify
from django.conf import settings
import os

from .models import Municipality, TouristSpot, Review, Rating, TouristSpotImage
from .forms import (
    UserRegistrationForm, ReviewForm, RatingForm,
    MunicipalityForm, TouristSpotForm
)

# ======================================================
# ✅ Helper Function
# ======================================================
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

# ======================================================
# ✅ WELCOME & AUTHENTICATION VIEWS
# ======================================================
def welcome_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    return render(request, 'tourism/welcome.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'tourism/login.html')


def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('admin_dashboard')
        else:
            return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False  # Ensure new users are regular users by default
            user.is_superuser = False
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'tourism/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


# ======================================================
# ✅ USER VIEWS
# ======================================================
@login_required
def home_view(request):
    municipalities = Municipality.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        tourist_spots = TouristSpot.objects.filter(
            Q(name__icontains=search_query) | 
            Q(municipality__name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    else:
        tourist_spots = TouristSpot.objects.all()[:6]
    
    context = {
        'municipalities': municipalities,
        'tourist_spots': tourist_spots,
        'search_query': search_query,
    }
    return render(request, 'tourism/home.html', context)


@login_required
def municipality_detail(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    tourist_spots = municipality.tourist_spots.all()
    
    context = {
        'municipality': municipality,
        'tourist_spots': tourist_spots,
    }
    return render(request, 'tourism/municipality_detail.html', context)


@login_required
def tourist_spot_detail(request, spot_id):
    tourist_spot = get_object_or_404(TouristSpot, id=spot_id)
    reviews = tourist_spot.reviews.all().order_by('-created_at')
    review_form = ReviewForm()
    rating_form = RatingForm()

    if request.method == 'POST':
        if 'review' in request.POST:
            review_form = ReviewForm(request.POST, request.FILES)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.tourist_spot = tourist_spot
                review.user = request.user
                review.save()
                messages.success(request, 'Review posted successfully!')
                return redirect('tourist_spot_detail', spot_id=spot_id)

        elif 'submit_rating' in request.POST or 'rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating, created = Rating.objects.get_or_create(
                    tourist_spot=tourist_spot,
                    user=request.user,
                    defaults={'rating': rating_form.cleaned_data['rating']}
                )
                if not created:
                    rating.rating = rating_form.cleaned_data['rating']
                    rating.save()
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'ok': True,
                        'average': round(tourist_spot.average_rating, 1),
                        'userRating': rating.rating,
                        'count': tourist_spot.ratings.count(),
                    })
                messages.success(request, 'Rating submitted successfully!')
                return redirect('tourist_spot_detail', spot_id=spot_id)

    if request.method != 'POST':
        existing_rating = Rating.objects.filter(tourist_spot=tourist_spot, user=request.user).first()
        if existing_rating:
            rating_form = RatingForm(initial={'rating': existing_rating.rating})

    gallery_images = []
    # Add main image first if exists
    if tourist_spot.image:
        if 'RENDER' in os.environ:
            # In production, use static path
            gallery_images.append(tourist_spot.image.url.replace('/media/', ''))
        else:
            gallery_images.append(tourist_spot.image.url)
    
    # Add gallery images
    for extra_image in tourist_spot.images.all():
        if extra_image.image:
            if 'RENDER' in os.environ:
                gallery_images.append(extra_image.image.url.replace('/media/', ''))
            else:
                gallery_images.append(extra_image.image.url)

    # Add images from img folder (moved from tourist_spot_gallery)
    if 'RENDER' in os.environ:
        # In production, look in static img folder
        static_dir = os.path.join(settings.BASE_DIR, 'static', 'img')
    else:
        # In development, look in media folder
        static_dir = os.path.join(settings.MEDIA_ROOT, 'tourist_spot_gallery')
    
    slug = slugify(tourist_spot.name)
    if os.path.isdir(static_dir):
        try:
            for fname in sorted(os.listdir(static_dir)):
                if fname.lower().startswith(slug) or tourist_spot.name.lower() in fname.lower():
                    if 'RENDER' in os.environ:
                        gallery_images.append('img/' + fname)
                    else:
                        gallery_images.append(settings.MEDIA_URL.rstrip('/') + '/tourist_spot_gallery/' + fname)
                if len(gallery_images) >= 10:
                    break
        except Exception:
            pass

    # Add review images
    for r in reviews:
        if r.image:
            if 'RENDER' in os.environ:
                gallery_images.append(r.image.url.replace('/media/', ''))
            else:
                gallery_images.append(r.image.url)
        if len(gallery_images) >= 15:
            break

    preset_coords = {
        'naval spring resort': (11.5794, 124.3966),
        'tinago falls - biliran': (11.5370, 124.5554),
        'sambawan island': (11.8230, 124.3306),
        'ulan ulan falls': (11.5512, 124.6103),
        'mainit hot spring': (11.5587, 124.6059),
        'agta beach': (11.6333, 124.4333),
        'marienor resort': (11.5728, 124.3925),
        'lucsoon cold spring': (11.5805, 124.4007),
        'higatangan island': (11.5825, 124.3261),
        'casyawan falls': (11.5689, 124.4152),
    }

    lat, lng = 11.5853, 124.4750
    if tourist_spot.latitude and tourist_spot.longitude:
        lat, lng = tourist_spot.latitude, tourist_spot.longitude
    else:
        name_key = tourist_spot.name.lower().strip()
        if name_key in preset_coords:
            lat, lng = preset_coords[name_key]

    all_spots_in_municipality = TouristSpot.objects.filter(
        municipality=tourist_spot.municipality
    ).exclude(id=tourist_spot.id)

    context = {
        'tourist_spot': tourist_spot,
        'reviews': reviews,
        'review_form': review_form,
        'rating_form': rating_form,
        'gallery_images': gallery_images,
        'map_lat': lat,
        'map_lng': lng,
        'all_spots_in_municipality': all_spots_in_municipality,
    }
    return render(request, 'tourism/tourist_spot_detail.html', context)


@login_required
def search_results(request):
    query = request.GET.get('q', '')
    if query:
        tourist_spots = TouristSpot.objects.filter(
            Q(name__icontains=query) | 
            Q(municipality__name__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        tourist_spots = TouristSpot.objects.all()
    
    context = {'tourist_spots': tourist_spots, 'query': query}
    return render(request, 'tourism/search_results.html', context)


# ======================================================
# ✅ LOGO AND ADS CORNER VIEWS
# ======================================================
@login_required
def logo_page(request):
    return render(request, 'tourism/logo_page.html')


@login_required
def poster_page(request):
    return render(request, 'tourism/poster_page.html')


@login_required
def advertisement_page(request):
    return render(request, 'tourism/advertisement_page.html')


# ======================================================
# ✅ ADMIN VIEWS
# ======================================================
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    from django.contrib.auth.models import User
    
    municipalities_count = Municipality.objects.count()
    tourist_spots_count = TouristSpot.objects.count()
    reviews_count = Review.objects.count()
    ratings_count = Rating.objects.count()
    users_count = User.objects.count()

    recent_spots = TouristSpot.objects.all().order_by('-created_at')[:5]
    recent_reviews = Review.objects.all().order_by('-created_at')[:5]
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    context = {
        'municipalities_count': municipalities_count,
        'tourist_spots_count': tourist_spots_count,
        'reviews_count': reviews_count,
        'ratings_count': ratings_count,
        'users_count': users_count,
        'recent_spots': recent_spots,
        'recent_reviews': recent_reviews,
        'recent_users': recent_users,
    }
    return render(request, 'tourism/admin_dashboard.html', context)


# ----------------- Municipality Management -----------------
@login_required
@user_passes_test(is_admin)
def admin_municipality_list(request):
    municipalities = Municipality.objects.all()
    return render(request, 'tourism/admin_municipality_list.html', {'municipalities': municipalities})


@login_required
@user_passes_test(is_admin)
def admin_municipality_add(request):
    if request.method == 'POST':
        form = MunicipalityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Municipality added successfully!')
            return redirect('admin_municipality_list')
    else:
        form = MunicipalityForm()
    return render(request, 'tourism/admin_municipality_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def admin_municipality_edit(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    if request.method == 'POST':
        form = MunicipalityForm(request.POST, request.FILES, instance=municipality)
        if form.is_valid():
            form.save()
            messages.success(request, 'Municipality updated successfully!')
            return redirect('admin_municipality_list')
    else:
        form = MunicipalityForm(instance=municipality)
    return render(request, 'tourism/admin_municipality_form.html', {'form': form, 'municipality': municipality, 'action': 'Edit'})


@login_required
@user_passes_test(is_admin)
def admin_municipality_delete(request, municipality_id):
    municipality = get_object_or_404(Municipality, id=municipality_id)
    if request.method == 'POST':
        municipality.delete()
        messages.success(request, 'Municipality deleted successfully!')
        return redirect('admin_municipality_list')
    return render(request, 'tourism/admin_municipality_delete.html', {'municipality': municipality})


# ----------------- Tourist Spot Management -----------------
@login_required
@user_passes_test(is_admin)
def admin_tourist_spot_list(request):
    tourist_spots = TouristSpot.objects.all().select_related('municipality')
    return render(request, 'tourism/admin_tourist_spot_list.html', {'tourist_spots': tourist_spots})


@login_required
@user_passes_test(is_admin)
def admin_tourist_spot_add(request):
    if request.method == 'POST':
        form = TouristSpotForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tourist spot added successfully!')
            return redirect('admin_tourist_spot_list')
    else:
        form = TouristSpotForm()
    return render(request, 'tourism/admin_tourist_spot_form.html', {'form': form, 'action': 'Add'})


@login_required
@user_passes_test(is_admin)
def admin_tourist_spot_edit(request, spot_id):
    tourist_spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == 'POST':
        form = TouristSpotForm(request.POST, request.FILES, instance=tourist_spot)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tourist spot updated successfully!')
            return redirect('admin_tourist_spot_list')
    else:
        form = TouristSpotForm(instance=tourist_spot)

    lat = tourist_spot.latitude if tourist_spot.latitude else 11.5853
    lng = tourist_spot.longitude if tourist_spot.longitude else 124.4750

    return render(request, 'tourism/admin_tourist_spot_form.html', {
        'form': form,
        'tourist_spot': tourist_spot,
        'action': 'Edit',
        'map_lat': lat,
        'map_lng': lng,
    })


@login_required
@user_passes_test(is_admin)
def admin_tourist_spot_delete(request, spot_id):
    tourist_spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == 'POST':
        tourist_spot.delete()
        messages.success(request, 'Tourist spot deleted successfully!')
        return redirect('admin_tourist_spot_list')
    return render(request, 'tourism/admin_tourist_spot_delete.html', {'tourist_spot': tourist_spot})


@login_required
@user_passes_test(is_admin)
def admin_tourist_spot_map_edit(request, spot_id):
    tourist_spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == 'POST':
        lat = request.POST.get('latitude')
        lng = request.POST.get('longitude')
        if lat and lng:
            tourist_spot.latitude = float(lat)
            tourist_spot.longitude = float(lng)
            tourist_spot.save()
            messages.success(request, 'Map coordinates updated successfully!')
            return redirect('admin_tourist_spot_edit', spot_id=spot_id)
        else:
            messages.error(request, 'Invalid coordinates.')

    lat = tourist_spot.latitude if tourist_spot.latitude else 11.5853
    lng = tourist_spot.longitude if tourist_spot.longitude else 124.4750

    return render(request, 'tourism/admin_tourist_spot_map_edit.html', {
        'tourist_spot': tourist_spot,
        'map_lat': lat,
        'map_lng': lng,
    })


# ----------------- Reviews Management -----------------
@login_required
@user_passes_test(is_admin)
def admin_reviews_list(request):
    reviews = Review.objects.all().select_related('user', 'tourist_spot').order_by('-created_at')
    return render(request, 'tourism/admin_reviews_list.html', {'reviews': reviews})


@login_required
@user_passes_test(is_admin)
def admin_review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('admin_reviews_list')
    return render(request, 'tourism/admin_review_delete.html', {'review': review})


# ----------------- User Management -----------------
@login_required
@user_passes_test(is_admin)
def admin_users_list(request):
    from django.contrib.auth.models import User
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'tourism/admin_users_list.html', {'users': users})


# ----------------- Image Management -----------------
@login_required
@user_passes_test(is_admin)
def admin_images_manage(request):
    from .models import TouristSpotImage
    tourist_spots = TouristSpot.objects.all().select_related('municipality').prefetch_related('images')
    return render(request, 'tourism/admin_images_manage.html', {'tourist_spots': tourist_spots})


@login_required
@user_passes_test(is_admin)
def admin_add_images(request, spot_id):
    from .models import TouristSpotImage
    tourist_spot = get_object_or_404(TouristSpot, id=spot_id)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                TouristSpotImage.objects.create(
                    tourist_spot=tourist_spot,
                    image=image
                )
            messages.success(request, f'{len(images)} image(s) added successfully to {tourist_spot.name}!')
        else:
            messages.error(request, 'Please select at least one image.')
    return redirect('admin_images_manage')


@login_required
@user_passes_test(is_admin)
def admin_delete_image(request, image_id):
    from .models import TouristSpotImage
    image = get_object_or_404(TouristSpotImage, id=image_id)
    if request.method == 'POST':
        spot_name = image.tourist_spot.name
        image.delete()
        messages.success(request, f'Image deleted successfully from {spot_name}!')
    return redirect('admin_images_manage')
