Static branding
---------------

Place your logo and hero background images here so the UI matches your brand:

1. Create directory `static/img/` (already referenced in templates)
2. Save files:
   - `static/img/logo.png`  → your circular Explore Biliran logo
   - `static/img/hero.jpg`  → the red bridge scenic photo for background

Run the server and hard-refresh if the images don’t appear.

# Explore Biliran - Tourism Website

A Django-based tourism website for exploring the beautiful island of Biliran, Philippines.

## Features

- **User Authentication**: Login and registration system
- **Municipality Exploration**: Browse through all 8 municipalities of Biliran
- **Tourist Spot Details**: View detailed information about tourist attractions
- **Search Functionality**: Search for tourist spots, municipalities, or attractions
- **Reviews & Ratings**: Users can post reviews, ratings, and upload photos
- **Modern UI**: Beautiful, responsive design with Bootstrap 5

## Municipalities Included

1. **Naval** - The capital municipality
2. **Almeria** - Coastal municipality
3. **Kawayan** - Agricultural lands
4. **Maripipi** - Island municipality
5. **Culaba** - Peaceful landscapes
6. **Caibiran** - Hot springs
7. **Cabucgayan** - Cultural heritage
8. **Biliran** - Namesake municipality

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd ExploreBil
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django pillow
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate database with sample data**
   ```bash
   python manage.py populate_data
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the website**
   - Open your browser and go to: `http://127.0.0.1:8000/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

## Usage

### For Users
1. **Register/Login**: Create an account or login to access the website
2. **Browse Municipalities**: Click on any municipality to see its tourist spots
3. **Search**: Use the search bar to find specific tourist spots
4. **View Details**: Click on tourist spots to see detailed information
5. **Rate & Review**: Leave ratings and reviews for tourist spots you've visited
6. **Upload Photos**: Share your experience with photos in reviews

### For Administrators
1. **Access Admin Panel**: Login to `/admin/` with your superuser credentials
2. **Manage Content**: Add, edit, or delete municipalities and tourist spots
3. **Upload Images**: Add images for municipalities and tourist spots
4. **Monitor Reviews**: View and manage user reviews and ratings

## Project Structure

```
ExploreBil/
├── explore_biliran/          # Main Django project
├── tourism/                  # Tourism app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── forms.py             # Form classes
│   ├── admin.py             # Admin configuration
│   └── templates/tourism/   # HTML templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── manage.py               # Django management script
└── README.md               # This file
```

## Models

- **Municipality**: Stores information about Biliran's municipalities
- **TouristSpot**: Contains details about tourist attractions
- **Review**: User reviews with comments and optional images
- **Rating**: User ratings (1-5 stars) for tourist spots

## Technologies Used

- **Backend**: Django 5.2.5
- **Frontend**: Bootstrap 5, Font Awesome
- **Database**: SQLite (default)
- **Image Processing**: Pillow

## Customization

### Adding New Tourist Spots
1. Login to the admin panel
2. Go to "Tourist spots" section
3. Click "Add tourist spot"
4. Fill in the details and upload an image
5. Save

### Adding Municipality Images
1. Login to the admin panel
2. Go to "Municipalities" section
3. Edit the municipality
4. Upload an image
5. Save

## Contributing

Feel free to contribute to this project by:
- Adding more tourist spots
- Improving the UI/UX
- Adding new features
- Fixing bugs

## License

This project is open source and available under the MIT License.
