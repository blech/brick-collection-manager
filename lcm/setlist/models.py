from django.db import models
from django.utils.html import format_html
from django.utils.http import urlencode

class OwnedSet(models.Model):
    collection_id = models.IntegerField(unique=True, verbose_name="Collection ID")
    set_number =    models.CharField(max_length=10, verbose_name="Number")
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
        verbose_name = "Owned set"

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

    def set_thumb(self):
        return "<img src='http://www.1000steine.com/brickset/thumbs/tn_%s_jpg.jpg'>" % self.set_number
    set_thumb.allow_tags = True

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


class CatalogueSet(models.Model):
    setID = models.IntegerField(verbose_name='Brickset ID')
    number = models.CharField(max_length=10)
    numberVariant = models.IntegerField(default=1)
    setName = models.CharField(max_length=128, verbose_name='Name')
    year = models.IntegerField(default=0)
    theme = models.CharField(max_length=64)
    subtheme = models.CharField(max_length=64, default='')
    pieces = models.IntegerField(null=True)
    minifigs = models.IntegerField(null=True)
    image = models.BooleanField(default=False)
    imageFilename = models.CharField(max_length=32, verbose_name="Image Filename")
    thumbnailURL = models.URLField(verbose_name="Thumbnail URL")
    imageURL = models.URLField(verbose_name="Image URL")
    bricksetURL = models.URLField(verbose_name="Brickset URL")
    own = models.BooleanField(default=False, verbose_name="Own?")
    want = models.BooleanField(default=False, verbose_name="Want?")
    qtyOwned = models.IntegerField(default=0, verbose_name="Owned")
    userNotes = models.CharField(max_length=128, default='')
    UKRetailPrice = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    USRetailPrice = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    CARetailPrice = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    instructionsAvailable = models.BooleanField(default=False, verbose_name="Instructions?")
    EAN = models.CharField(max_length=16, default='')
    UPC = models.CharField(max_length=16, default='')
    lastUpdated = models.DateTimeField(null=True)

    class Meta:
        ordering = ('number', 'numberVariant')

    def __unicode__(self):
        return self.set_number()

    def set_number(self):
        return "%s-%s" % (self.number, self.numberVariant)
    set_number.admin_order_field = 'number'
    set_number.short_description = 'Set'

    def viewtheme(self):
        if self.subtheme:
            subtheme = self.subtheme
            if '/' in subtheme:
                subtheme = subtheme.replace('/', ' / ')
            return "%s / %s" % (self.theme, subtheme)
        return self.theme

    viewtheme.short_description = 'Theme / Subthemes'
    viewtheme.admin_order_field = 'theme'
    viewtheme.allow_tags = True
