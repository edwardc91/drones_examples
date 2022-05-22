from django.contrib import admin
from base import models


@admin.register(models.Drone)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'model', 'state', 'battery_capacity')
    list_filter = ('model', 'state')
    search_fields = ['serial_number', 'model', 'state']


@admin.register(models.Medication)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'weight',)
    search_fields = ['name', 'code',]


@admin.register(models.DroneStatusLog)
class DroneAdmin(admin.ModelAdmin):
    list_display = ('drone_name', 'current_battery', 'created',)
    search_fields = ['drone_name',]
    date_hierarchy = 'created'

