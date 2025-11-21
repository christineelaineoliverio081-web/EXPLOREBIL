# Manual Tourist Spots Guide

## How to Add Your Own Tourist Spots

You have complete control over what tourist spots to include in your website. Here's how to manually add them:

### 1. Access Django Admin

1. **Start the server** (if not already running):
   ```
   python manage.py runserver
   ```

2. **Go to admin panel**: http://127.0.0.1:8000/admin/

3. **Login** with your admin credentials

### 2. Add Municipalities First

1. **Click on "Municipalities"** in the admin panel
2. **Click "Add Municipality"**
3. **Fill in the details**:
   - **Name**: (e.g., "Naval", "Almeria", "Kawayan", etc.)
   - **Description**: Brief description of the municipality
   - **Image**: (Optional) Upload an image for the municipality
4. **Click "Save"**

### 3. Add Tourist Spots

1. **Click on "Tourist spots"** in the admin panel
2. **Click "Add Tourist spot"**
3. **Fill in the details**:
   - **Name**: Your tourist spot name (e.g., "Naval Spring Resort")
   - **Municipality**: Select which municipality it belongs to
   - **Description**: Detailed description of the tourist spot
   - **Image**: Upload an image for this tourist spot
   - **Address**: Specific address or location
4. **Click "Save"**

### 4. Add Images for Tourist Spots

For each tourist spot you create, you can:

1. **Upload directly** through the admin interface when creating/editing the tourist spot
2. **Or use the image system** I set up:
   - Save your image in `media/tourist_spots/`
   - Name it to match the tourist spot (e.g., `naval_spring_resort.jpg`)
   - Update the templates to include the image path

### 5. Example: Adding "Naval Spring Resort"

1. **In Admin Panel**:
   - Name: "Naval Spring Resort"
   - Municipality: Select "Naval"
   - Description: "A beautiful spring resort with natural pools..."
   - Address: "Naval, Biliran"
   - Image: Upload your image

2. **For the image system**:
   - Save your image as `naval_spring_resort.jpg` in `media/tourist_spots/`
   - The templates will automatically show it

### 6. Remove Sample Data (Optional)

If you want to start fresh:

1. **Delete existing tourist spots** through the admin panel
2. **Or run this command** to clear all data:
   ```
   python manage.py flush
   ```
   (This will clear ALL data, including users)

### 7. Your Complete Control

- ✅ **Add any tourist spots** you want
- ✅ **Choose the exact names** you prefer
- ✅ **Select which municipalities** they belong to
- ✅ **Write your own descriptions**
- ✅ **Upload your own images**
- ✅ **Delete or edit** anytime through admin

### 8. Current Admin Features

- **Tourist Spots**: Add, edit, delete tourist spots
- **Municipalities**: Add, edit, delete municipalities
- **Reviews**: View and delete reviews (admin can delete)
- **Ratings**: View ratings (admin cannot delete)

### 9. Image Paths for Your Tourist Spots

When you add tourist spots, you can set up image paths like this:

```html
{% elif tourist_spot.name == 'Your Tourist Spot Name' %}
    <img src="/media/tourist_spots/your_image_name.jpg" class="card-img-top" alt="Your Tourist Spot Name">
```

**This is YOUR website - you decide what tourist spots to include!**
