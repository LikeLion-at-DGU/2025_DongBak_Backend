from django.conf import settings
from .models import *
from rest_framework import serializers

from django.core.exceptions import FieldDoesNotExist

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

# class HashTagSerializer(serializers.ModelSerializer):
#     booth = serializers.PrimaryKeyRelatedField(queryset=Booth.objects.all())

#     class Meta:
#         model = HashTag
#         fields = ['id', 'booth', 'name']

class FoodTruckImageSerializer(serializers.ModelSerializer):
    food_truck = serializers.PrimaryKeyRelatedField(queryset=FoodTruck.objects.all())
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = FoodTruckImage
        fields = ['id', 'food_truck', 'image']
    

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
    
    # hash_tag = serializers.SerializerMethodField()
    # def get_hash_tag(self, obj):
    #     tags = obj.tags.all()
    #     return HashTagSerializer(instance=tags, many = True, context=self.context).data
    
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    # start_recruitment = serializers.SerializerMethodField()
    # end_recruitment = serializers.SerializerMethodField()
    # def get_start_recruitment(self, obj):
    #     if obj.start_recruitment:
    #         # 날짜 형식 (월) + 요일을 가져오기
    #         return obj.start_recruitment.strftime("%m월 %d일 (%a)").replace("Mon", "월").replace("Tue", "화").replace("Wed", "수").replace("Thu", "목").replace("Fri", "금").replace("Sat", "토").replace("Sun", "일")
    #     return None
    # def get_end_recruitment(self, obj):
    #     if obj.end_recruitment:
    #         return obj.end_recruitment.strftime("%m월 %d일 (%a)").replace("Mon", "월").replace("Tue", "화").replace("Wed", "수").replace("Thu", "목").replace("Fri", "금").replace("Sat", "토").replace("Sun", "일")
    #     return None
    
    day = serializers.PrimaryKeyRelatedField(
        queryset=Day.objects.all(), many=True, write_only=True
    )
    day_display = DaySerializer(many=True, read_only=True, source="day")

    club_name_intro = serializers.SerializerMethodField()
    club_name_with = serializers.SerializerMethodField()
    
    def get_josa(self, word, josa1, josa2):
        """받침 유무에 따라 조사를 선택하는 함수"""
        if not word:
            return None
        
        last_char = word[-1]  # 마지막 글자 추출
        last_char_code = ord(last_char)  # 유니코드 변환

        if 0xAC00 <= last_char_code <= 0xD7A3:  # 한글 범위 내인지 확인
            jongseong = (last_char_code - 0xAC00) % 28  # 종성(받침) 체크
            return josa2 if jongseong == 0 else josa1  # 받침 없으면 josa2, 받침 있으면 josa1
        
        return josa2  # 한글이 아니면 기본적으로 받침 없음 취급

    def get_club_name_intro(self, obj):
        """'을/를'을 적용한 문장 생성"""
        josa = self.get_josa(obj.club_name, "을", "를")
        return f"{obj.club_name}{josa} 소개해요!" if obj.club_name else None

    def get_club_name_with(self, obj):
        """'와/과'를 적용한 문장 생성"""
        josa = self.get_josa(obj.club_name, "과", "와")
        return f"{obj.club_name}{josa} 함께해요!" if obj.club_name else None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name in representation.keys():
            if field_name in ["booth_image", "club_logo"]:  # `SerializerMethodField`는 모델 필드가 아님
                continue
            
            try:
                model_field = Booth._meta.get_field(field_name)
                if isinstance(model_field, models.TextField) and representation[field_name]:
                    # 개행 문자 제거 후 리스트 변환
                    cleaned_text = representation[field_name].replace("\r", "")  # \r 제거
                    representation[field_name] = cleaned_text.split("\n")  # \n 기준으로 리스트 변환
            except FieldDoesNotExist:
                continue  # 모델에 없는 필드는 무시
        return representation

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name in representation.keys():
            if field_name in ["food_truck_image"]:  # `SerializerMethodField`는 모델 필드가 아님
                continue
            
            try:
                model_field = FoodTruck._meta.get_field(field_name)
                if isinstance(model_field, models.TextField) and representation[field_name]:
                    # 개행 문자 제거 후 리스트 변환
                    cleaned_text = representation[field_name].replace("\r", "")  # \r 제거
                    representation[field_name] = cleaned_text.split("\n")  # \n 기준으로 리스트 변환
            except FieldDoesNotExist:
                continue  # 모델에 없는 필드는 무시
        return representation
