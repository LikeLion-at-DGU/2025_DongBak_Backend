from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Booth(models.Model):
    BOOTH_DAY = [
        (None, ''),
        ('(수)', '(수)'),
        ('(목)', '(목)')
    ]
    BOOTH_LOCATION = [
        (None, ''),
        ('만해광장', '만해광장'),
        ('팔정도', '팔정도')
    ]
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=50)
    booth_name = models.CharField(max_length=50)
    day = models.CharField(max_length=20, choices=BOOTH_DAY, default='')
    location = models.CharField(max_length=30, choices=BOOTH_LOCATION, default='')
    booth_num = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    club_logo = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    club_category = models.CharField(max_length=20)
    club_discription = models.CharField(max_length=250, blank=True, null=True)
    booth_discription = models.CharField(max_length=250, blank=True, null=True)
    start_recruitment = models.DateField()
    end_recruitment = models.DateField()
    apply_method = models.CharField(max_length=300)
    insta_url = models.CharField(max_length=200, blank=True, null=True)

class FoodTruck(models.Model):
    FOODTRUCK_DAY = [
        (None, ''),
        ('(수)', '(수)'),
        ('(목)', '(목)')
    ]
    FOODTRUCK_LOCATION = [
        (None, ''),
        ('만해광장', '만해광장'),
        ('팔정도', '팔정도')
    ]
    id = models.AutoField(primary_key=True)
    food_truck_name = models.CharField(max_length=50)
    day = models.CharField(max_length=20, choices=FOODTRUCK_DAY, default='')
    location = models.CharField(max_length=30, choices=FOODTRUCK_LOCATION, default='')
    food_truck_num = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    food_truck_discription = models.CharField(max_length=400)
    insta_url = models.URLField(max_length=200, blank=True, null=True)

class BoothImage(models.Model):
    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

class FoodTruckImage(models.Model):
    id = models.AutoField(primary_key=True)
    food_truck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

class HashTag(models.Model):
    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='tags')
    name = models.CharField(max_length=50)
