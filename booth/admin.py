from django.contrib import admin
from .models import *

# 1️⃣ Booth 이미지를 Inline으로 설정
class BoothImageInline(admin.TabularInline):
    model = BoothImage
    extra = 1       # 기본 1개 폼 표시
    max_num = None  # 제한 없이 ‘+’ 버튼으로 계속 추가 가능
    fields = ["image"]

# 2️⃣ Booth 관리자 페이지 설정
class BoothAdmin(admin.ModelAdmin):
    list_display = ("id", "booth_name", "club_name", "location")
    inlines = [BoothImageInline]

# 3️⃣ FoodTruck 이미지를 Inline으로 설정
class FoodTruckImageInline(admin.TabularInline):
    model = FoodTruckImage
    extra = 1       # 기본 1개 폼 표시
    max_num = None  # 제한 없이 ‘+’ 버튼으로 계속 추가 가능
    fields = ["image"]

# 4️⃣ FoodTruck 관리자 페이지 설정
class FoodTruckAdmin(admin.ModelAdmin):
    list_display = ("id", "food_truck_name", "location")
    inlines = [FoodTruckImageInline]

# 5️⃣ Admin에 등록
admin.site.register(Day)
admin.site.register(Booth, BoothAdmin)
admin.site.register(FoodTruck, FoodTruckAdmin)