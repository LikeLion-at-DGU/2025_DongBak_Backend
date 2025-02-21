from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().order_by('start_time')
    serializer_class = PerformanceSerializer

    @action(detail=False, methods=["get"], url_path="wednesday")
    def wednesday_booths(self, request):
        """수요일 부스만 필터링하여 location별 그룹화"""
        performances = self.get_queryset().filter(day=1)
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 공연만 필터링"""
        performances = self.get_queryset().filter(day=2)
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)