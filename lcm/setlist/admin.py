from django.contrib import admin
from .models import LegoSet

class LegoSetAdmin(admin.ModelAdmin):
    list_display = ('set_number', 'set_name', 'chain', 'vendor', 'online', 'used', 
                    'date_acquired', 'total_price')
    list_filter = ('theme', 'subtheme', 'date_acquired')
    ordering = ('-date_acquired',)
admin.site.register(LegoSet, LegoSetAdmin)

