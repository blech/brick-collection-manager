from django.contrib import admin
from django.utils.html import format_html

from .models import LegoSet

class LegoSetAdmin(admin.ModelAdmin):
    list_display = ('set_number', 'set_name', 'bought', 'viewtheme', 'online', 
                    'new', 'date_acquired', 'total_price')
    list_filter = ('date_acquired', 'chain', 'theme')
    list_per_page = 20
    ordering = ('-date_acquired',)

    def get_actions(self, request):
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(LegoSet, LegoSetAdmin)

