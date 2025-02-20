from django.conf import settings
from .models import *
from rest_framework import serializers

class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ['name']
    

class BoothImageSerializer(serializers.ModelSerializer):
    booth = serializers.PrimaryKeyRelatedField(queryset=Booth.objects.all())
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = BoothImage
        fields = ['id', 'booth', 'image']

class HashTagSerializer(serializers.ModelSerializer):
    booth = serializers.PrimaryKeyRelatedField(queryset=Booth.objects.all())

    class Meta:
        model = HashTag
        fields = ['id', 'booth', 'name']

class FoodTruckImageSerializer(serializers.ModelSerializer):
    food_truck = serializers.PrimaryKeyRelatedField(queryset=FoodTruck.objects.all())
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = FoodTruckImage
        fields = ['id', 'food_truck', 'image']
    
    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    

class BoothSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = '__all__'
        read_only_fields = [
            'id',
        ]
    club_logo = serializers.ImageField(use_url=True, required=False)

    booth_image = serializers.SerializerMethodField()
    def get_booth_image(self, obj):
        image = obj.image.all()
        return BoothImageSerializer(instance=image, many=True, context=self.context).data
    
    hash_tag = serializers.SerializerMethodField()
    def get_hash_tag(self, obj):
        tags = obj.tags.all()
        return HashTagSerializer(instance=tags, many = True, context=self.context).data
    
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    start_recruitment = serializers.SerializerMethodField()
    end_recruitment = serializers.SerializerMethodField()
    def get_start_recruitment(self, obj):
        if obj.start_recruitment:
            # 날짜 형식 (월) + 요일을 가져오기
            return obj.start_recruitment.strftime("%m월 %d일 (%a)").replace("Mon", "월").replace("Tue", "화").replace("Wed", "수").replace("Thu", "목").replace("Fri", "금").replace("Sat", "토").replace("Sun", "일")
        return None
    def get_end_recruitment(self, obj):
        if obj.end_recruitment:
            return obj.end_recruitment.strftime("%m월 %d일 (%a)").replace("Mon", "월").replace("Tue", "화").replace("Wed", "수").replace("Thu", "목").replace("Fri", "금").replace("Sat", "토").replace("Sun", "일")
        return None
    
    day = serializers.PrimaryKeyRelatedField(
        queryset=Day.objects.all(), many=True, write_only=True
    )
    day_display = DaySerializer(many=True, read_only=True, source="day")

class BoothListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booth
        fields = ['id', 'booth_image', 'booth_name', 'club_name', 'day', 'start_time', 'end_time', 'location', 'booth_num']
        read_only_fields = ['id']

    booth_image = serializers.SerializerMethodField()
    def get_booth_image(self, obj):
        first_image = obj.image.first()
        return BoothImageSerializer(instance=first_image, context=self.context).data if first_image else None
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    day = serializers.SerializerMethodField()
    def get_day(self, instance):
        serializer = DaySerializer(instance.day.all(), many=True)
        return serializer.data


class FoodTruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodTruck
        fields = '__all__'
        read_only_fields = ['id']
    food_truck_image = serializers.SerializerMethodField()
    def get_food_truck_image(self, obj):
        request = self.context.get('request')
        image = obj.image.all()
        return FoodTruckImageSerializer(instance=image, many=True, context=self.context).data
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    day = serializers.PrimaryKeyRelatedField(
        queryset=Day.objects.all(), many=True, write_only=True
    )
    day_display = DaySerializer(many=True, read_only=True, source="day")
