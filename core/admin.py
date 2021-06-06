from django.contrib import admin

from core.models import Pet, Lot, Bid


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'kind', 'breed', 'owner']
    ordering = ['name']
    search_fields = ['name', 'owner__first_name', 'owner__last_name']
    list_filter = ['kind', 'breed']


@admin.register(Lot)
class LotAdmin(admin.ModelAdmin):
    list_display = ['id', 'pet', 'price', 'status', 'owner']
    list_filter = ['status', 'pet__kind', 'pet__breed']


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'owner', 'lot']
    search_fields = ['owner_first_name', 'owener__last_name']
    list_filter = ['lot']
