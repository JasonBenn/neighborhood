from django.contrib.gis import admin
from django.contrib.gis.geos import Point

from houses.models import Person, Rater, Rating


class RaterAdmin(admin.ModelAdmin):
    list_display = ("name",)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("value", "rater_id", "created")
    ordering = ("-created",)
    list_filter = ('rater__name', 'value')

    def get_list_filter(self, request):
        return super().get_list_filter(request)


class PersonAdmin(admin.GISModelAdmin):
    gis_widget_kwargs = {'attrs': {
        "default_lon": -122.435451,
        "default_lat": 37.767,
        "default_zoom": 15,
        "map_width": 900,
        "map_height": 750,
    }}

admin.site.register(Rating, RatingAdmin)
admin.site.register(Rater, RaterAdmin)
admin.site.register(Person, PersonAdmin)
