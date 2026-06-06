from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Hair, Nail, Product



@override_settings(
    # Avoid WhiteNoise manifest lookup errors in tests.
    STORAGES={
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
    }
)
class ViewTests(TestCase):
    def setUp(self):
        # Minimal in-memory image to satisfy ImageField.
        self.image = SimpleUploadedFile(
            name="test.jpg",
            content=b"\xff\xd8\xff\xe0" + b"0" * 1024,  # not a real jpeg, but sufficient for storage validation
            content_type="image/jpeg",
        )

        self.product1 = Product.objects.create(
            name="Product 1",
            price=10,
            description="Desc 1",
            image=self.image,
        )
        self.product2 = Product.objects.create(
            name="Product 2",
            price=20,
            description="Desc 2",
            image=self.image,
        )

        self.hair1 = Hair.objects.create(
            name="Hair 1",
            price=5,
            description="Hair Desc 1",
            image=self.image,
        )

        self.nail1 = Nail.objects.create(
            name="Nail 1",
            price=7,
            description="Nail Desc 1",
            image=self.image,
        )
        self.nail2 = Nail.objects.create(
            name="Nail 2",
            price=9,
            description="Nail Desc 2",
            image=self.image,
        )

    def test_home_renders_and_context_counts(self):
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

        self.assertIn("products", resp.context)
        self.assertIn("hairs", resp.context)
        self.assertIn("nails", resp.context)

        self.assertEqual(resp.context["products"].count(), 2)
        self.assertEqual(resp.context["hairs"].count(), 1)
        self.assertEqual(resp.context["nails"].count(), 2)

    def test_products_renders_and_context(self):
        url = reverse("products")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("products", resp.context)
        self.assertEqual(resp.context["products"].count(), 2)

    def test_services_renders_and_context_counts(self):
        url = reverse("services")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("hairs", resp.context)
        self.assertIn("nails", resp.context)
        self.assertEqual(resp.context["hairs"].count(), 1)
        self.assertEqual(resp.context["nails"].count(), 2)

    def test_smoke_routes_return_200(self):
        # Smoke tests for the remaining routes.
        for name in [
            "about",
            "header",
            "database",
            "cart_detail",

            "data_structure",
        ]:
            with self.subTest(route=name):
                resp = self.client.get(reverse(name))
                self.assertEqual(resp.status_code, 200)

    def test_add_product_to_cart(self):
        resp = self.client.post(
            reverse("cart_add", args=["product", self.product1.id]),
            {"quantity": 2},
        )
        self.assertRedirects(resp, reverse("cart_detail"))
        self.assertEqual(self.client.session["cart"][f"product:{self.product1.id}"], 2)

    def test_cart_supports_hair_and_nail_items(self):
        self.client.post(reverse("cart_add", args=["hair", self.hair1.id]))
        self.client.post(reverse("cart_add", args=["nail", self.nail1.id]))

        resp = self.client.get(reverse("cart_detail"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context["cart_total"], self.hair1.price + self.nail1.price)
        self.assertEqual(len(resp.context["cart_entries"]), 2)

    def test_update_and_remove_cart_item(self):
        self.client.post(reverse("cart_add", args=["product", self.product1.id]))

        self.client.post(
            reverse("cart_update", args=["product", self.product1.id]),
            {"quantity": 3},
        )
        self.assertEqual(self.client.session["cart"][f"product:{self.product1.id}"], 3)

        self.client.post(reverse("cart_remove", args=["product", self.product1.id]))
        self.assertNotIn(f"product:{self.product1.id}", self.client.session["cart"])

