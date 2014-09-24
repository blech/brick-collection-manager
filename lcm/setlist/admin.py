import logging

from django.contrib import admin
from django.db.models import *

from .models import OwnedSet, CatalogueSet

class OwnedSetAdmin(admin.ModelAdmin):
    change_list_template = 'changelist_total.html'
    list_display = ('set_thumb', 'set_number', 'set_name', 'bought', 'viewtheme', 'online', 
                    'new', 'date_acquired', 'price')
    list_per_page = 20
    date_hierarchy = 'date_acquired'
    ordering = ('-date_acquired',)

    def changelist_view(self, request, extra_context=None):
        response = super(OwnedSetAdmin, self).changelist_view(request, extra_context)

        if hasattr(response, 'context_data'):
            context_list = response.context_data["cl"]
    
            full_queryset = context_list.query_set
            total = full_queryset.aggregate(total=Sum('total_price'))
            page = sum([s.total_price for s in context_list.result_list])
    
            my_context = {'page_price': page, 'total_price': total['total']}
    
            response.context_data.update(my_context)
        return response

    def get_actions(self, request):
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(OwnedSet, OwnedSetAdmin)

class CatalogueSetAdmin(admin.ModelAdmin):
    list_display = ('set_number', 'setName', 'viewtheme', 'own', 'want', 'pieces', 'minifigs', 
                    'year', 'USRetailPrice')
    list_per_page = 20
    ordering = ('-year', '-pieces')

    def get_actions(self, request):
        return []

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(CatalogueSet, CatalogueSetAdmin)
