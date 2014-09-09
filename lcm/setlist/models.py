from django.db import models
from django.utils.html import format_html
from django.utils.http import urlencode

class LegoSet(models.Model):
    collection_id = models.IntegerField(unique=True)
    set_number =    models.CharField(max_length=10, verbose_name="Set")
    set_name =      models.CharField(max_length=128, verbose_name="Name")
    theme =         models.CharField(max_length=64)
    subtheme =      models.CharField(max_length=64)
    year =          models.CharField(max_length=4, blank=True)
    date_acquired = models.DateField(null=True, verbose_name="Acquired")
    acquired_from = models.CharField(max_length=64)
    price_paid =    models.DecimalField(max_digits=6, decimal_places=2, default="0.00")

    additional_price_paid = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    current_estimated = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    condition_when_acquired = models.CharField(max_length=16)

    condition_now = models.CharField(max_length=16)
    location =      models.CharField(max_length=32)
    parts =         models.BooleanField(default=False)
    minifigs =      models.BooleanField(default=False)
    instructions =  models.BooleanField(default=False)
    box =           models.BooleanField(default=False)
    will_trade =    models.BooleanField(default=False)
    notes =         models.TextField()
    deleted =       models.BooleanField(default=False)

    online =        models.BooleanField(default=False)
    used =          models.BooleanField(default=False)
    total_price =   models.DecimalField(max_digits=6, decimal_places=2, default="0.00", 
                        verbose_name="Total")
    chain =         models.CharField(max_length=32)
    vendor =        models.CharField(max_length=32)

    class Meta:
        ordering = ('-date_acquired',)
        verbose_name = "Lego set"

    def __unicode__(self):
        return self.set_number

    def _build_filter_link(self, filter, subfilter=None):
        link = format_html("<a href='?{0}'>{1}</a>",
                        urlencode({filter['field']: filter['value']}),
                        filter.get('display') or filter['value'])

        if subfilter:
            link += ' / '
            link += format_html("<a href='?{0}'>{1}</a>",
                        urlencode({filter['field']: filter['value'], 
                                   subfilter['field']: subfilter['value']}),
                        subfilter.get('display') or subfilter['value'])

        return link

    def bought(self):
        subfilter = False
        if self.vendor:
            subfilter = {'field': 'vendor', 'value': self.vendor,}
        filter = {'field': 'chain', 'value': self.chain,}
        return self._build_filter_link(filter, subfilter)

    bought.short_description = "Acquired From"
    bought.admin_order_field = 'chain'
    bought.allow_tags = True

    def new(self):
        return not self.used
    new.boolean = True
    new.admin_order_field = 'used'

    def price(self):
        return "$%.2f" % self.total_price
    price.admin_order_field = 'total_price'

    def viewtheme(self):
        subfilter = False
        if self.subtheme:
            subfilter = {'field': 'subtheme', 'value': self.subtheme,}
            if '/' in self.subtheme:
                subfilter['display'] = self.subtheme.replace('/', ' / ')

        filter = {'field': 'theme', 'value': self.theme}

        return self._build_filter_link(filter, subfilter)

    viewtheme.short_description = 'Theme / Subthemes'
    viewtheme.admin_order_field = 'theme'
    viewtheme.allow_tags = True


