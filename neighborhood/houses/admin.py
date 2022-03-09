from django.contrib import admin

from houses.models import Rater, Rating


class RaterAdmin(admin.ModelAdmin):
    list_display = ("name",)


admin.site.register(Rater, RaterAdmin)
admin.site.register(Rating)