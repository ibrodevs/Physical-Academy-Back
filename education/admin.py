from django.contrib import admin
from .models import (
    Master,
    Phd,
    PhdStuff,
    MasterStuff,
    CollegeDepartmentInfo,
    CollegeTabCategory,
    CollegeManagement,
)

# Register existing models

class MasterStuffInline(admin.TabularInline):
    model = MasterStuff

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    inlines = [MasterStuffInline]


class PhdStuffInline(admin.TabularInline):
    model = PhdStuff

@admin.register(Phd)
class PhdAdmin(admin.ModelAdmin):
    inlines = [PhdStuffInline]




admin.site.register(CollegeTabCategory)
admin.site.register(CollegeDepartmentInfo)
admin.site.register(CollegeManagement)
