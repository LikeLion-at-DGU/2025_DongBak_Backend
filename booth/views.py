from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import *
from .serializers import *

class BoothViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == "foodtruck_by_day":
            return FoodTruck.objects.all()
        return Booth.objects.all()
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
        booths = self.get_queryset().filter(day="(수)")
        serialized_booths = self.get_serializer(booths, many=True).data
        return Response(self.group_by_location(serialized_booths))

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 부스만 필터링하여 location별 그룹화"""
        booths = self.get_queryset().filter(day="(목)")
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
        day_map = {"wednesday": "(수)", "thursday": "(목)"}
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
        food_trucks = self.get_queryset().filter(day="(수)")
        serialized_food_trucks = self.get_serializer(food_trucks, many=True).data
        return Response(self.group_by_location(serialized_food_trucks))

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 푸드트럭만 필터링하여 location별 그룹화"""
        food_trucks = self.get_queryset().filter(day="(목)")
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