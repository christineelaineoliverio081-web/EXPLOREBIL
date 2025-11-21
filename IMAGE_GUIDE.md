# Image Guide for Tourist Spots

## How to Add Images to Tourist Spots

I've set up the system so you can easily add specific images for each tourist spot. Here's how it works:

### 1. Image Directory
All tourist spot images should be placed in: `media/tourist_spots/`

### 2. Current Image Paths Set Up
The following image paths are already configured in the templates:

- **Naval Spring Resort**: `/media/tourist_spots/naval_spring_resort.jpg`
- **Almeria Beach**: `/media/tourist_spots/almeria_beach.jpg`
- **Kawayan Falls**: `/media/tourist_spots/kawayan_falls.jpg`
- **Maripipi Beach**: `/media/tourist_spots/maripipi_beach.jpg`
- **Culaba Hot Spring**: `/media/tourist_spots/culaba_hot_spring.jpg`
- **Culaba Falls**: `/media/tourist_spots/culaba_falls.jpg`
- **Caibiran Waterfall**: `/media/tourist_spots/caibiran_waterfall.jpg`
- **Cabucgayan Beach**: `/media/tourist_spots/cabucgayan_beach.jpg`
- **Biliran Church**: `/media/tourist_spots/biliran_church.jpg`

### 3. How to Add Your Images

1. **Prepare your images** (JPG, PNG, etc.)
2. **Rename them** to match the paths above
3. **Place them** in the `media/tourist_spots/` folder

### 4. Adding More Tourist Spots

If you want to add images for more tourist spots, you need to:

1. **Add the image** to `media/tourist_spots/`
2. **Update the templates** by adding a new condition in both:
   - `tourism/templates/tourism/tourist_spot_detail.html`
   - `tourism/templates/tourism/municipality_detail.html`

### 5. Example: Adding a New Tourist Spot Image

If you have a new tourist spot called "Naval Beach", you would:

1. Save your image as `naval_beach.jpg` in `media/tourist_spots/`
2. Add this condition to both template files:
   ```html
   {% elif spot.name == 'Naval Beach' %}
       <img src="/media/tourist_spots/naval_beach.jpg" class="card-img-top" alt="Naval Beach" style="height: 200px; object-fit: cover;">
   ```

### 6. Multiple Images for One Tourist Spot

If you want to show multiple images for one tourist spot, you can modify the templates to include multiple image tags or create an image gallery.

### 7. Image Requirements
- **Format**: JPG, PNG, GIF, etc.
- **Size**: Recommended around 800x600 pixels or larger
- **File size**: Keep under 5MB for good performance

### 8. Current Tourist Spots in Database
Based on the sample data, these tourist spots exist:
- Naval Spring Resort (Naval)
- Almeria Beach (Almeria)
- Kawayan Falls (Kawayan)
- Maripipi Beach (Maripipi)
- Culaba Hot Spring (Culaba)
- Culaba Falls (Culaba)
- Caibiran Waterfall (Caibiran)
- Cabucgayan Beach (Cabucgayan)
- Biliran Church (Biliran)

Just add your images with the exact names shown above, and they will automatically appear on the website!
