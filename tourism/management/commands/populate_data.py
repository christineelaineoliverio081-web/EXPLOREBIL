from django.core.management.base import BaseCommand
from tourism.models import Municipality, TouristSpot

class Command(BaseCommand):
    help = 'Populate the database with sample municipalities and tourist spots'

    def handle(self, *args, **options):
        # Create Municipalities
        municipalities_data = [
            {
                'name': 'Naval',
                'description': 'The capital municipality of Biliran province, known for its beautiful beaches and historical sites.'
            },
            {
                'name': 'Almeria',
                'description': 'A coastal municipality famous for its pristine beaches and fishing industry.'
            },
            {
                'name': 'Kawayan',
                'description': 'Known for its agricultural lands and scenic mountain views.'
            },
            {
                'name': 'Maripipi',
                'description': 'An island municipality with stunning beaches and crystal clear waters.'
            },
            {
                'name': 'Culaba',
                'description': 'A peaceful municipality with beautiful landscapes and waterfalls.'
            },
            {
                'name': 'Caibiran',
                'description': 'Known for its hot springs and natural attractions.'
            },
            {
                'name': 'Cabucgayan',
                'description': 'A municipality with rich cultural heritage and natural beauty.'
            },
            {
                'name': 'Biliran',
                'description': 'The namesake municipality of the province, home to many tourist attractions.'
            }
        ]

        for data in municipalities_data:
            municipality, created = Municipality.objects.get_or_create(
                name=data['name'],
                defaults={'description': data['description']}
            )
            if created:
                self.stdout.write(f'Created municipality: {municipality.name}')

        # Create Tourist Spots
        tourist_spots_data = [
            {
                'name': 'Ulan-Ulan Falls',
                'municipality': 'Naval',
                'description': 'A majestic waterfall surrounded by lush greenery, perfect for nature lovers and adventure seekers.',
                'address': 'Naval, Biliran'
            },
            {
                'name': 'Tinago Falls',
                'municipality': 'Almeria',
                'description': 'A hidden gem with crystal clear waters and a serene atmosphere.',
                'address': 'Almeria, Biliran'
            },
            {
                'name': 'Mainit Hot Spring',
                'municipality': 'Caibiran',
                'description': 'Natural hot springs known for their therapeutic properties and relaxing environment.',
                'address': 'Caibiran, Biliran'
            },
            {
                'name': 'Higatangan Island',
                'municipality': 'Naval',
                'description': 'A beautiful island with white sand beaches and clear blue waters.',
                'address': 'Naval, Biliran'
            },
            {
                'name': 'Biliran Bridge',
                'municipality': 'Biliran',
                'description': 'An iconic bridge connecting Biliran to Leyte, offering spectacular views.',
                'address': 'Biliran, Biliran'
            },
            {
                'name': 'Maripipi Beach',
                'municipality': 'Maripipi',
                'description': 'Pristine beaches with powdery white sand and turquoise waters.',
                'address': 'Maripipi, Biliran'
            },
            {
                'name': 'Kawayan Rice Terraces',
                'municipality': 'Kawayan',
                'description': 'Beautiful terraced rice fields showcasing traditional farming methods.',
                'address': 'Kawayan, Biliran'
            },
            {
                'name': 'Culaba Falls',
                'municipality': 'Culaba',
                'description': 'A serene waterfall perfect for swimming and picnicking.',
                'address': 'Culaba, Biliran'
            },
            {
                'name': 'Cabucgayan Heritage Site',
                'municipality': 'Cabucgayan',
                'description': 'Historical sites and cultural landmarks preserving local heritage.',
                'address': 'Cabucgayan, Biliran'
            }
        ]

        for data in tourist_spots_data:
            municipality = Municipality.objects.get(name=data['municipality'])
            tourist_spot, created = TouristSpot.objects.get_or_create(
                name=data['name'],
                municipality=municipality,
                defaults={
                    'description': data['description'],
                    'address': data['address']
                }
            )
            if created:
                self.stdout.write(f'Created tourist spot: {tourist_spot.name} in {municipality.name}')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
