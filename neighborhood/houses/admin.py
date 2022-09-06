from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from houses.models import Building, Event, Person, Rater, Rating


class RaterAdmin(admin.ModelAdmin):
    list_display = ("name",)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("value", "rater_id", "created")
    ordering = ("-created",)
    list_filter = ('rater__name', 'value')

    def get_list_filter(self, request):
        return super().get_list_filter(request)

gis_kwargs = {
    "default_lon": -122.435451,
    "default_lat": 37.767,
    "default_zoom": 15,
    "map_width": 900,
    "map_height": 750,
}

class PersonAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {'attrs': gis_kwargs}
    # list_filter = ('building')
    # list_display = ("name", "building")


class BuildingAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {'attrs': gis_kwargs}


class EventAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {'attrs': gis_kwargs}


admin.site.register(Rating, RatingAdmin)
admin.site.register(Rater, RaterAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Event, EventAdmin)
