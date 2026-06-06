from django.db import models


class Header(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Item(models.Model):
    CATEGORY_COSMETIC = "cosmetic"
    CATEGORY_HAIR = "hair"
    CATEGORY_NAILS = "nails"

    CATEGORY_CHOICES = [
        (CATEGORY_COSMETIC, "Cosmetic"),
        (CATEGORY_HAIR, "Hair"),
        (CATEGORY_NAILS, "Nails"),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    # Common fields
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="img/")

    # Optional fields for hair/nails
    details_title = models.CharField(max_length=120, blank=True, default="")
    included = models.TextField(blank=True, default="")
    aftercare = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


    



    from django.db import models

