from .models import *
from rest_framework import serializers
from booth.serializers import DaySerializer

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields ='__all__'
    
    start_time = serializers.TimeField(format="%H:%M")
    end_time = serializers.TimeField(format="%H:%M")

    songs = serializers.SerializerMethodField(read_only=True)
    def get_songs(self, instance):
        serializer = SongSerializer(instance.songs, context=self.context, many=True)
        return serializer.data
    
    members = serializers.SerializerMethodField(read_only=True)
    def get_members(self, instance):
        serializer = MemberSerializer(instance.members, context=self.context, many=True)
        return serializer.data
    
    day = serializers.PrimaryKeyRelatedField(
        queryset=Day.objects.all(), many=True, write_only=True
    )
    day_display = DaySerializer(many=True, read_only=True, source="day")
    
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'