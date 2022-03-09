from django.contrib import admin

from houses.models import Rater, Rating


class RaterAdmin(admin.ModelAdmin):
    list_display = ("name",)


class RatingAdmin(admin.ModelAdmin):
    list_display = ("value", "rater_id", "created")
    ordering = ("-created",)
    list_filter = ('rater__name', 'value')

    def get_list_filter(self, request):
        return super().get_list_filter(request)


admin.site.register(Rating, RatingAdmin)
admin.site.register(Rater, RaterAdmin)