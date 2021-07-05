
from django.db import models
from store_auth.models import StoreAuth


class MenuItem(models.Model):
    page_access_token   = models.ForeignKey(StoreAuth, on_delete=models.CASCADE)
    item_name           = models.CharField(max_length=300, null=False)
    item_price          = models.FloatField()
    item_image_url      = models.URLField(null=True)
    item_description    = models.CharField(max_length=300, null=True)
    times_ordered       = models.IntegerField(default=0)
    created_time        = models.DateTimeField(auto_now_add=True)


