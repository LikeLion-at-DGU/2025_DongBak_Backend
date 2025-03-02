from django.apps import AppConfig
from django.db.models.signals import post_migrate

def set_foodtruck_initial_id(sender, **kwargs):
    from booth.models import FoodTruck
    if not FoodTruck.objects.exists():
        FoodTruck.objects.create(id=99, food_truck_name="dummy", food_truck_num=1, start_time="10:00", end_time="20:00", food_truck_description="temp")
        FoodTruck.objects.filter(id=99).delete()

class BoothConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booth'

    def ready(self):
        post_migrate.connect(set_foodtruck_initial_id, sender=self)