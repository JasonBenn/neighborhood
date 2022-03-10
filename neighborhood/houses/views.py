import json
from uuid import UUID

from django.http import HttpResponse
from django.shortcuts import render

import utils
from houses.models import Rater, Rating, ZillowSnapshot
from django.db import connection

from houses.queries import LEADERBOARD, NEXT_LISTINGS, NUM_HOUSES_BY_TYPE
from utils import fetchall


def index(request):
    listings = [{**x, **{
        'filenames': json.loads(x['filenames'])
    }} for x in fetchall(NEXT_LISTINGS)]

    return render(request, "ratings.html", {
        "listings": listings,
        "raters": Rater.objects.all(),
        "leaderboard": fetchall(LEADERBOARD),
        "active_rater_id": request.session.get('active_rater_id'),
        "is_leaderboard_hidden": request.session.get('is_leaderboard_hidden')
    })


def analytics(request):
    houses_by_type = fetchall(NUM_HOUSES_BY_TYPE)
    houses_by_type.append({"use_definition": "Total", "count": sum([x["count"] for x in houses_by_type])})
    return render(request, "analytics.html", {
        "houses_by_type": houses_by_type
    })


def create_rating(request):
    data = json.loads(request.body)
    rater_id = int(data['raterId'])
    zillow_id = UUID(data['zillowSnapshotId'])
    Rating.objects.create(
        rater_id=rater_id,
        zillow_snapshot_id=zillow_id,
        zillow_scraped_address=ZillowSnapshot.objects.get(id=zillow_id).scraped_address,
        value=int(data['value']) if data['value'] else None,
    )
    request.session['active_rater_id'] = rater_id
    request.session['is_leaderboard_hidden'] = bool(data['isLeaderboardHidden'])
    print(request.session['is_leaderboard_hidden'])
    return HttpResponse(status=204)
