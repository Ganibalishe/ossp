from django.contrib import admin

from road.models import Point, Section, Road


class PointInLine(admin.TabularInline):
    model = Point
    extra = 0


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [PointInLine]


class SectionInLine(admin.TabularInline):
    model = Section
    extra = 0


@admin.register(Road)
class RoadAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [SectionInLine]

