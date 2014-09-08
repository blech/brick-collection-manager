import logging

from django.contrib import admin
from django.db.models import *

from .models import LegoSet

class LegoSetAdmin(admin.ModelAdmin):
    change_list_template = 'changelist_total.html'
    list_display = ('set_number', 'set_name', 'bought', 'viewtheme', 'online', 
                    'new', 'date_acquired', 'total_price')
    list_per_page = 20
    ordering = ('-date_acquired',)

    def changelist_view(self, request, extra_context=None):
        response = super(LegoSetAdmin, self).changelist_view(request, extra_context)

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

admin.site.register(LegoSet, LegoSetAdmin)

