from django.db import models

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

    def __unicode__(self):
        return self.set_number

    class Meta:
        ordering = ('-date_acquired',)

