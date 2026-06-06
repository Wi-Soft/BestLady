from django.contrib import admin

from myapp.models import Header, Item


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")
    search_fields = ("title", "subtitle")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "price",
        "image",
        "details_title",
    )
    list_filter = ("category", "price")
    ordering = ("category", "name")
    search_fields = (
        "name",
        "description",
        "included",
        "aftercare",
        "notes",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "category",
                    "name",
                    "price",
                    "description",
                    "image",
                )
            },
        ),
        (
            "Extra details (Hair/Nails)",
            {
                "fields": (
                    "details_title",
                    "included",
                    "aftercare",
                    "notes",
                )
            },
        ),
    )



