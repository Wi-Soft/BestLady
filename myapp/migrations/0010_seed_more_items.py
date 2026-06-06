from django.db import migrations


def seed_more_items(apps, schema_editor):
    Item = apps.get_model('myapp', 'Item')

    # Idempotent: only create items missing by (category, name)
    existing = set(Item.objects.values_list('category', 'name'))

    img1 = 'img/1.jpg'
    img2 = 'img/2.jpg'
    img3 = 'img/6.webp'
    img4 = 'img/beuty_clinic.jpg'
    img5 = 'img/lemme-play.webp'

    items = [
        # Cosmetics (additional)
        {
            'category': 'cosmetic',
            'name': 'Soft Matte Lip Kit',
            'price': 2100,
            'description': 'Long-wearing matte lip color with a smooth, soft finish.',
            'image': img5,
        },
        {
            'category': 'cosmetic',
            'name': 'Hydrating Face Mist',
            'price': 1900,
            'description': 'Lightweight mist that refreshes and helps keep skin hydrated.',
            'image': img4,
        },
        {
            'category': 'cosmetic',
            'name': 'Daily SPF Defense',
            'price': 2600,
            'description': 'Everyday sun protection to help protect and brighten your skin.',
            'image': img3,
        },

        # Hair (additional)
        {
            'category': 'hair',
            'name': 'Repair & Restore Mask',
            'price': 3800,
            'description': 'A focused mask treatment to improve softness and strength.',
            'image': img1,
            'details_title': 'Includes',
            'included': 'Pre-treatment cleanse • mask application • blow-dry finish',
            'aftercare': 'Use sulfate-free shampoo and apply mask weekly.',
            'notes': 'Great before events.',
        },
        {
            'category': 'hair',
            'name': 'Scalp Refresh + Wash',
            'price': 2900,
            'description': 'Relaxing scalp cleanse with moisturizing finish.',
            'image': img2,
            'details_title': 'What’s included',
            'included': 'Scalp scrub • wash • conditioning • styling tips',
            'aftercare': 'Avoid heavy oils for 24h after service.',
            'notes': 'Helps reduce dryness and buildup.',
        },
        {
            'category': 'hair',
            'name': 'Trim & Shape Styling',
            'price': 2400,
            'description': 'A clean trim and shape with a polished, everyday style.',
            'image': img5,
            'details_title': 'Includes',
            'included': 'Trim • shape • blow-dry • styling guidance',
            'aftercare': 'Use heat protectant and moisturize ends regularly.',
            'notes': 'Perfect for maintaining growth.',
        },

        # Nails (additional)
        {
            'category': 'nails',
            'name': 'Nail Art Accent Session',
            'price': 2200,
            'description': 'Simple nail art accents to elevate your manicure.',
            'image': img2,
            'details_title': 'Includes',
            'included': 'Basic manicure • 1–2 accent designs • finish coat',
            'aftercare': 'Wear gloves, avoid soaking your nails for long periods.',
            'notes': 'Designs chosen during consultation.',
        },
        {
            'category': 'nails',
            'name': 'Natural Strengthening Treatment',
            'price': 2400,
            'description': 'Strengthen and smooth your natural nails for a healthier look.',
            'image': img1,
            'details_title': 'Includes',
            'included': 'Nail prep • strengthening base • buff + polish',
            'aftercare': 'Keep nails moisturized and avoid biting.',
            'notes': 'Perfect if your nails peel or break easily.',
        },
    ]

    for data in items:
        key = (data['category'], data['name'])
        if key in existing:
            continue
        Item.objects.create(**data)


class Migration(migrations.Migration):
    dependencies = [
        ('myapp', '0009_seed_items'),
    ]

    operations = [
        migrations.RunPython(seed_more_items, reverse_code=migrations.RunPython.noop),
    ]

