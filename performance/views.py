from rest_framework import viewsets,status
from .models import *
from .serializers import *
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.views import APIView
import os
from django.conf import settings
import pandas as pd
import json
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all().order_by('start_time')
    serializer_class = PerformanceSerializer

    @action(detail=False, methods=["get"], url_path="wednesday")
    def wednesday_booths(self, request):
        """수요일 부스만 필터링하여 location별 그룹화"""
        performances = self.get_queryset().filter(day=1)
        serializer = PerformanceSerializer(performances, context= {'request':request}, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="thursday")
    def thursday_booths(self, request):
        """목요일 공연만 필터링"""
        performances = self.get_queryset().filter(day=2)
        serializer = PerformanceSerializer(performances, context= {'request':request}, many=True)
        return Response(serializer.data)
    
class PerformanceDataView(APIView):
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
            "동아리명", "공연 분야", "공연 시작시간", "공연 종료시간", "인스타 url", "day", "곡", "멤버"
        ]
        if not all(col in df.columns for col in required_columns):
            return Response({"error": "CSV 파일에 필요한 모든 열이 포함되지 않았습니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        Performance.objects.all().delete()  # 기존 데이터 삭제

        performance_data = {}
        for _, row in df.iterrows():
            performance = Performance.objects.create(
                club_name=row["동아리명"],
                category=row["공연 분야"],
                start_time=row["공연 시작시간"],
                end_time=row["공연 종료시간"],
                insta_url=row["인스타 url"]
            )

            days = row["day"].split(",")
            for day_name in days:
                day_obj, created = Day.objects.get_or_create(name=day_name.strip())
                performance.day.add(day_obj)

            song_names = row["곡"].split(",") if pd.notna(row["곡"]) else []
            for song_name in song_names:
                Song.objects.create(performance=performance, name=song_name.strip())

            # Member 추가
            member_names = row["멤버"].split(",") if pd.notna(row["멤버"]) else []
            for member_name in member_names:
                Member.objects.create(performance=performance, name=member_name.strip())

            performance_data[performance.id] = {
                "동아리명": row["동아리명"],
                "공연 분야": row["공연 분야"],
                "공연 시작시간": row["공연 시작시간"],
                "공연 종료시간": row["공연 종료시간"],
                "인스타 url": row["인스타 url"],
                "day": days,
                "곡": song_names,
                "멤버": member_names
            }

        return Response(performance_data, status=status.HTTP_200_OK)