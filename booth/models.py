from django.db import models

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Day(models.Model):
    DAY_CHOICES = [
        (None, ''),
        ('수', '(수)'),
        ('목', '(목)')
    ]
    name = models.CharField(max_length=10, choices=DAY_CHOICES, default='', unique=True)

    def __str__(self):
        return self.name

class Booth(models.Model):
    BOOTH_LOCATION = [
        (None, ''),
        ('만해광장', '만해광장'),
        ('팔정도', '팔정도')
    ]
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=50)
    booth_name = models.CharField(max_length=50)
    day = models.ManyToManyField(Day)
    location = models.CharField(max_length=30, choices=BOOTH_LOCATION, default='')
    booth_num = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    club_logo = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    club_category = models.CharField(max_length=20)
    club_description = models.TextField(blank=True, null=True)
    booth_description = models.TextField(blank=True, null=True)
    # start_recruitment = models.DateField(blank=True, null=True)
    # end_recruitment = models.DateField(blank=True, null=True)
    recruitment = models.CharField(max_length=150, blank=True, null=True)
    apply_method = models.TextField()
    insta_url = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Django Admin에서 부스 이름을 대표로 표시하도록 설정
        """
        return self.booth_name

class FoodTruck(models.Model):
    FOODTRUCK_LOCATION = [
        (None, ''),
        ('만해광장', '만해광장'),
        ('팔정도', '팔정도')
    ]
    id = models.BigAutoField(primary_key=True)
    food_truck_name = models.CharField(max_length=50)
    day = models.ManyToManyField(Day)
    location = models.CharField(max_length=30, choices=FOODTRUCK_LOCATION, default='')
    food_truck_num = models.IntegerField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    food_truck_description = models.CharField(max_length=400)
    insta_url = models.URLField(max_length=200, blank=True, null=True)
    booth_num = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:  # 새 객체인 경우
            last_instance = FoodTruck.objects.order_by('-id').first()
            if last_instance and last_instance.id < 100:
                self.id = 100
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Django Admin에서 푸드트럭 이름을 대표로 표시하도록 설정
        """
        return self.food_truck_name

class BoothImage(models.Model):
    id = models.AutoField(primary_key=True)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

class FoodTruckImage(models.Model):
    id = models.AutoField(primary_key=True)
    food_truck = models.ForeignKey(FoodTruck, on_delete=models.CASCADE, related_name='image')
    image = models.ImageField(upload_to=image_upload_path, null=True, blank=True)

# class HashTag(models.Model):
#     id = models.AutoField(primary_key=True)
#     booth = models.ForeignKey(Booth, on_delete=models.CASCADE, related_name='tags')
#     name = models.CharField(max_length=50)
