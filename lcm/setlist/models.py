from django.db import models

class LegoSet(models.Model):
    collection_id = models.IntegerField(unique=True)
    set_number = models.CharField(max_length=10)
    set_name = models.CharField(max_length=128)
    theme = models.CharField(max_length=64)
    subtheme = models.CharField(max_length=64)
    year = models.CharField(max_length=4, blank=True)
    date_acquired = models.DateField(null=True)
    acquired_from = models.CharField(max_length=64)
    price_paid = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    additional_price_paid = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    current_estimated = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    condition_when_acquired = models.CharField(max_length=16)
    condition_now = models.CharField(max_length=16)
    location = models.CharField(max_length=32)
    parts = models.BooleanField(default=False)
    minifigs = models.BooleanField(default=False)
    instructions = models.BooleanField(default=False)
    box = models.BooleanField(default=False)
    will_trade = models.BooleanField(default=False)
    notes = models.TextField()
    deleted = models.BooleanField(default=False)

    online = models.BooleanField(default=False)
    used = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default="0.00")
    chain = models.CharField(max_length=32)
    vendor = models.CharField(max_length=32)

    # 2546160
    # "75003-1"
    # "A-wing Starfighter"
    # "Star Wars"
    # "Episode IV-VI"
    # 2013
    # "2013-03-29"
    # "Target (online)"
    # "19.00"
    # "1.66"
    # "0.00"
    # "MISB"
    # "MISB"
    # ""
    # "Yes"
    # "Yes"
    # "Yes"
    # "Yes"
    # " "
    # ""
    # " "


