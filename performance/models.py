from django.db import models
from booth.models import Day

# Create your models here.
def image_upload_path(instance, filename):
    return f'{instance.pk}/{filename}'

class Performance(models.Model):
    # PERFORMANCE_LOCATION = [
    #     (None, ''),
    #     ('만해광장', '만해광장'),
    #     ('팔정도', '팔정도')
    # ]
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=30)
    day = models.ManyToManyField(Day)
    # location = models.CharField(max_length=30, choices=PERFORMANCE_LOCATION, default='')
    logo = models.ImageField(upload_to=image_upload_path, null=True, blank=True)
    category = models.CharField(max_length=30)
    start_time = models.TimeField()
    end_time = models.TimeField()
    insta_url = models.CharField(max_length=200)

    def __str__(self):
        return self.club_name

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='songs')
    name = models.TextField()

class Member(models.Model):
    id = models.AutoField(primary_key=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, related_name='members')
    name = models.TextField()