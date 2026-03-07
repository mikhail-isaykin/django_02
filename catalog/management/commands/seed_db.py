from django.core.management.base import BaseCommand
from catalog.models import Category, Product, ProductImage
import random
import urllib.request
from django.core.files.base import ContentFile
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Seeds the database with eyewear categories and products.'

    def handle(self, *args, **kwargs):
        self.stdout.write('Deleting existing data...')
        Category.objects.all().delete()
        Product.objects.all().delete()

        # 1. Create Categories
        glasses = Category.objects.create(name='Glasses', slug='glasses')
        sunglasses = Category.objects.create(name='Sunglasses', slug='sunglasses')
        self.stdout.write(self.style.SUCCESS('Categories created.'))

        product_names = [
            'Gamot 02', 'Musubi 02', 'Origami 031', 'La Cha 01(C)',
            'Limes 02', 'Boba 02', 'Lolos 02', 'Kota 02'
        ]
        
        frame_colors = ['Black', 'Silver', 'Gold', 'Clear', 'Tortoise']
        lens_colors = ['Clear', 'Grey', 'Brown', 'Green']
        materials = ['Acetate', 'Metal', 'Titanium']
        shapes = ['Square', 'Rectangle', 'Oval', 'Round']

        for name in product_names:
            category = random.choice([glasses, sunglasses])
            price = round(random.uniform(240.0, 300.0), 2)
            product = Product.objects.create(
                name=name,
                slug=slugify(name),
                price=price,
                category=category,
                description=f"A beautiful piece of eyewear: {name}.",
                frame_color=random.choice(frame_colors),
                lens_color=random.choice(lens_colors),
                frame_material=random.choice(materials),
                shape=random.choice(shapes),
                is_polarized=random.choice([True, False]),
                lens_width_mm=random.randint(48, 60),
                bridge_mm=random.randint(14, 22),
                frame_front_mm=random.randint(130, 150),
                temple_length_mm=random.randint(135, 150),
                lens_height_mm=random.randint(30, 50),
                fit_narrow_wide=random.randint(20, 80),
                fit_low_high=random.randint(20, 80)
            )

            # Generate a random placeholder image using LoremFlickr with 'glasses' keyword
            # To ensure it changes, we add a random lock parameter
            image_url = f"https://loremflickr.com/600/800/glasses,eyewear/all?lock={random.randint(1, 1000)}"
            try:
                # Add headers to avoid 403 Forbidden from some services
                req = urllib.request.Request(image_url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                if response.status == 200:
                    image_content = response.read()
                    file_name = f"{product.slug}.jpg"
                    
                    product_image = ProductImage(product=product, order=0)
                    product_image.image.save(file_name, ContentFile(image_content), save=True)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Could not download image for {name}: {e}"))

            self.stdout.write(f"Created product: {name}")

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
