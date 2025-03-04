from django.contrib import admin
from .models import Performance, Song, Member

# 1️⃣ Song & Member를 Performance에 Inline으로 연결
class SongInline(admin.TabularInline):
    model = Song
    extra = 1  # 기본 1개 폼 표시 (필요 시 'Add another Song'으로 추가 가능)

class MemberInline(admin.TabularInline):
    model = Member
    extra = 1  # 기본 1개 폼 표시 (필요 시 'Add another Member'로 추가 가능)

# 2️⃣ PerformanceAdmin에서 list_display에 요일 표시 + Inline 등록
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "club_name", "get_days", "start_time", "end_time")
    inlines = [SongInline, MemberInline]

    def get_days(self, obj):
        """
        Performance.day가 ManyToManyField로 여러 요일을 가질 수 있으므로,
        요일들(booth.models.Day)을 문자로 합쳐서 표시.
        """
        days = obj.day.all()  # ManyToMany Field (Day)
        return ", ".join(day.name for day in days)
    get_days.short_description = "Days"  # Admin 컬럼 헤더에 표시될 이름

# 3️⃣ 나머지 모델 단독 등록 (필요 시 Song, Member 제거 가능)
admin.site.register(Performance, PerformanceAdmin)