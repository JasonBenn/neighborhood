import json

from django.shortcuts import render

from neighborhood.settings import BASE_DIR


def index(request):
    context = json.loads(open(str(BASE_DIR / 'data/rating_dummy.json')).read())
    context['filenames'] = context['filenames'].split(', ')
    return render(request, "ratings.html", context)
