import json

from django.http import JsonResponse
from django.core import serializers
from constants import KEYS
from store_auth.models import StoreAuth
from menu.models import MenuItem


def menu_list(request):
    page_id = request.body.get(KEYS.PAGE_ID)
    store = StoreAuth.objects.get(page_id=page_id)
    menu_items = MenuItem.objects.filter(page_access_token=store)
    serialize_menu_items = json.loads(serializers.serialize('json', menu_items))
    menu_items_fields = [item.get(KEYS.FIELDS) for item in serialize_menu_items]
    return JsonResponse(menu_items_fields, status=200)