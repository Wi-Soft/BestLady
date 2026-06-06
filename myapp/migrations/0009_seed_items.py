from django.db import migrations


def seed_items(apps, schema_editor):
    Item = apps.get_model('myapp', 'Item')

    # If items already exist, do nothing.
    if Item.objects.exists():
        return

    img1 = 'img/1.jpg'
    img2 = 'img/2.jpg'
    img3 = 'img/6.webp'
    img4 = 'img/beuty_clinic.jpg'
    img5 = 'img/lemme-play.webp'

    items = [
        # Cosmetics
        {
            'category': 'cosmetic',
            'name': 'Cosmetic Starter Pack',
            'price': 2500,
            'description': 'A curated starter pack of your favorite cosmetics.',
            'image': img1,
        },
        {
            'category': 'cosmetic',
            'name': 'Glow Up Serum',
            'price': 3200,
            'description': 'Nourishing serum for a fresh and glowing finish.',
            'image': img2,
        },

        # Hair
        {
            'category': 'hair',
            'name': 'Hair Treatment Session',
            'price': 4500,
            'description': 'Deep conditioning + finishing for healthy hair.',
            'image': img4,
            'details_title': 'What you get',
            'included': 'Deep conditioning • styling • consultation',
            'aftercare': 'Hydrate daily, use gentle products.',
            'notes': 'Best for dry and damaged hair.',
        },

        # Nails
        {
            'category': 'nails',
            'name': 'Manicure & Polish',
            'price': 1800,
            'description': 'Clean manicure with long-lasting polish.',
            'image': img5,
            'details_title': 'Includes',
            'included': 'Cuticle care • shaping • polish',
            'aftercare': 'Wear gloves for cleaning, moisturize often.',
            'notes': 'Custom colors available.',
        },
        {
            'category': 'nails',
            'name': 'Gel Nails Set',
            'price': 2800,
            'description': 'A durable gel set for a clean and glossy look.',
            'image': img3,
            'details_title': 'Includes',
            'included': 'Gel application • shaping • finish',
            'aftercare': 'Avoid scraping, moisturize regularly.',
            'notes': 'Removal available on request.',
        },
    ]

    # Create rows
    for data in items:
        Item.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0008_item_delete_hair_delete_nail_delete_product'),
    ]

    operations = [
        migrations.RunPython(seed_items, reverse_code=migrations.RunPython.noop),
    ]

