from django.contrib import admin

from myapp.models import Header, Item


@admin.register(Header)
class HeaderAdmin(admin.ModelAdmin):
    list_display = ("title", "subtitle")


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price")
    list_filter = ("category",)
    search_fields = ("name", "description")


