from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db.models import Q
from .models import *
from .serializers import *

import os
from django.conf import settings
import pandas as pd
import json
from rest_framework.parsers import MultiPartParser, FormParser

class BoothViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == "foodtruck_by_day":
            return FoodTruck.objects.all().order_by('booth_num')
        return Booth.objects.all().order_by('booth_num')
    def get_serializer_class(self):
        if self.action in ["list", "wednesday_booths", "thursday_booths", "foodtruck_by_day"]:
            return BoothListSerializer
        return BoothSerializer

    def list(self, request, *args, **kwargs):
        """기본 부스 목록 조회 - location별 그룹화"""
        booths = self.get_queryset()
        serialized_booths = self.get_serializer(booths, many=True).data
        return Response(self.group_by_location(serialized_booths))

    @action(detail=False, methods=["get"], url_path="wednesday")
    def wednesday_booths(self, request):
        """수요일 부스만 필터링하여 location별 그룹화"""
        booths = self.get_queryset().filter(day=1)
        serialized_booths = self.get_serializer(booths, many=True).data
        return Response(self.group_by_location(serialized_booths))

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 부스만 필터링하여 location별 그룹화"""
        booths = self.get_queryset().filter(day=2)
        serialized_booths = self.get_serializer(booths, many=True).data
        return Response(self.group_by_location(serialized_booths))

    def group_by_location(self, booth_list):
        """location을 기준으로 JSON 데이터 그룹화"""
        grouped_booths = {}
        for booth in booth_list:
            location = booth["location"]
            if location not in grouped_booths:
                grouped_booths[location] = []
            grouped_booths[location].append(booth)
        return grouped_booths
    
    @action(detail=False, methods=["get"], url_path=r"(?P<day>\w+)/foodtruck")
    def foodtruck_by_day(self, request, day=None):
        """요일(day)별 푸드트럭 필터링하여 location별 그룹화"""
        day_map = {"wednesday": 1, "thursday": 2}
        if day not in day_map:
            return Response({"error": "Invalid day"}, status=400)

        food_trucks = FoodTruck.objects.filter(day=day_map[day])
        serialized_food_trucks = FoodTruckSerializer(food_trucks, many=True, context={'request': request}).data
        return Response(self.group_by_location(serialized_food_trucks))

    def group_by_location(self, food_truck_list):
        """location을 기준으로 JSON 데이터 그룹화"""
        grouped_food_trucks = {}
        for food_truck in food_truck_list:
            location = food_truck["location"]
            if location not in grouped_food_trucks:
                grouped_food_trucks[location] = []
            grouped_food_trucks[location].append(food_truck)
        return grouped_food_trucks

class FoodTruckViewSet(viewsets.ModelViewSet):
    queryset = FoodTruck.objects.all()
    serializer_class = FoodTruckSerializer

    def list(self, request, *args, **kwargs):
        """기본 부스 목록 조회 - location별 그룹화"""
        food_trucks = self.get_queryset()
        serialized_food_trucks = self.get_serializer(food_trucks, many=True).data
        return Response(self.group_by_location(serialized_food_trucks))

    @action(detail=False, methods=["get"], url_path="wednesday")
    def wednesday_booths(self, request):
        """수요일 푸드트럭만 필터링하여 location별 그룹화"""
        food_trucks = self.get_queryset().filter(day=1)
        serialized_food_trucks = self.get_serializer(food_trucks, many=True).data
        return Response(self.group_by_location(serialized_food_trucks))

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 푸드트럭만 필터링하여 location별 그룹화"""
        food_trucks = self.get_queryset().filter(day=2)
        serialized_food_trucks = self.get_serializer(food_trucks, many=True).data
        return Response(self.group_by_location(serialized_food_trucks))

    def group_by_location(self, food_truck_list):
        """location을 기준으로 JSON 데이터 그룹화"""
        grouped_food_trucks = {}
        for food_truck in food_truck_list:
            location =food_truck["location"]
            if location not in grouped_food_trucks:
                grouped_food_trucks[location] = []
            grouped_food_trucks[location].append(food_truck)
        return grouped_food_trucks
    
class SearchView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')

        if not query:
            return Response({"error": "검색어를 입력하세요."}, status=status.HTTP_400_BAD_REQUEST)

        # Booth 검색 (club_name, booth_name, booth_description)
        booth_results = Booth.objects.filter(
            Q(club_name__icontains=query) |
            Q(booth_name__icontains=query)
        ).distinct()

        # FoodTruck 검색 (food_truck_name, food_truck_description)
        food_truck_results = FoodTruck.objects.filter(
            Q(food_truck_name__icontains=query)
        ).distinct()

        booth_serializer = BoothListSerializer(booth_results, context = {'request': request}, many=True)
        food_truck_serializer = FoodTruckSerializer(food_truck_results, many=True)

        return Response({
            "booths": booth_serializer.data,
            "food_trucks": food_truck_serializer.data
        }, status=status.HTTP_200_OK)
    
class BoothDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        # CSV 파일 업로드 확인
        csv_file = request.FILES.get("file")
        if not csv_file:
            return Response({"error": "파일이 제공되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        # CSV 파일을 DataFrame으로 로드
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            return Response({"error": f"파일을 읽을 수 없습니다: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # 필수 컬럼 확인
        required_columns = [
            "부스 번호", "동아리명", "부스명", "부스 위치", "부스 시작시간", "부스 종료시간",
            "동아리 분과", "동아리 설명", "부스 설명", "모집 날짜", "지원 방법", "인스타 url", "day"
        ]
        if not all(col in df.columns for col in required_columns):
            return Response({"error": "CSV 파일에 필요한 모든 열이 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        Booth.objects.all().delete()  # 기존 데이터 삭제

        booth_data = {}
        for _, row in df.iterrows():
            booth_number = int(row["부스 번호"])
            booth = Booth.objects.create(
                booth_num=booth_number,
                club_name=row["동아리명"],
                booth_name=row["부스명"],
                location=row["부스 위치"],
                start_time=row["부스 시작시간"],
                end_time=row["부스 종료시간"],
                club_category=row["동아리 분과"],
                club_description=row["동아리 설명"],
                booth_description=row["부스 설명"],
                recruitment=row["모집 날짜"],
                # start_recruitment=row["모집 시작 날짜"],
                # end_recruitment=row["모집 종료 날짜"],
                apply_method=row["지원 방법"],
                insta_url=row["인스타 url"]
            )

            days = row["day"].split(",")
            for day_name in days:
                day_obj, created = Day.objects.get_or_create(name=day_name.strip())
                booth.day.add(day_obj)

            club_description_list = row["동아리 설명"].split("\n") if isinstance(row["동아리 설명"], str) else []
            booth_description_list = row["부스 설명"].split("\n") if isinstance(row["부스 설명"], str) else []

            booth_data[booth_number] = {
                "동아리명": row["동아리명"],
                "부스명": row["부스명"],
                "부스 위치": row["부스 위치"],
                "부스 시작시간": row["부스 시작시간"],
                "부스 종료시간": row["부스 종료시간"],
                "동아리 분과": row["동아리 분과"],
                "동아리 설명": club_description_list,
                "부스 설명": booth_description_list,
                "모집 날짜": row["모집 날짜"],
                # "모집 시작 날짜": row["모집 시작 날짜"],
                # "모집 종료 날짜": row["모집 종료 날짜"],
                "지원 방법": row["지원 방법"],
                "인스타 url": row["인스타 url"],
                "day": days 
            }

        return Response(booth_data, status=status.HTTP_200_OK)
