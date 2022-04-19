import json
from uuid import UUID

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render

from houses.models import Building, Person, Rater, Rating, ZillowSnapshot
from houses.queries import COUNT_RATINGS, LEADERBOARD, NEEDS_FIRST_RATING_COUNT, NEEDS_SECOND_RATING_COUNT, \
    NEEDS_THIRD_RATING_COUNT, \
    NEXT_LISTINGS, \
    NUM_HOUSES_BY_TYPE
from utils import execute_sql, fetchall


def get_denominator():
    return execute_sql(NEEDS_FIRST_RATING_COUNT) * 3 + execute_sql(NEEDS_SECOND_RATING_COUNT) * 2 + execute_sql(NEEDS_THIRD_RATING_COUNT) + execute_sql(COUNT_RATINGS)


def index(request):
    listings = [{**x, **{
        'filenames': json.loads(x['filenames'])
    }} for x in fetchall(NEXT_LISTINGS)]
    progress_numerator = Rating.objects.count()
    progress_denominator = get_denominator()

    if progress_numerator >= progress_denominator:
        return render(request, "thanks.html")

    return render(request, "ratings.html", {
        "listings": listings,
        "raters": Rater.objects.all(),
        "leaderboard": fetchall(LEADERBOARD),
        "progress_numerator": progress_numerator,
        "progress_denominator": progress_denominator,
        "progress": round(progress_numerator / progress_denominator * 100),
        "active_rater_id": request.session.get('active_rater_id'),
        "is_leaderboard_hidden": request.session.get('is_leaderboard_hidden')
    })


def thanks(request):
    return render(request, "thanks.html")


def analytics(request):
    houses_by_type = fetchall(NUM_HOUSES_BY_TYPE)
    houses_by_type.append({"use_definition": "Total", "count": sum([x["count"] for x in houses_by_type])})
    return render(request, "analytics.html", {
        "houses_by_type": houses_by_type
    })


def hoodmap(request):
    raw_people = Person.objects.all()
    people = serialize('geojson', raw_people, geometry_field='location', fields=('first_name', 'last_name'))
    raw_buildings = Building.objects.all()
    buildings = serialize('geojson', raw_buildings, geometry_field='location', fields=('name',))
    return render(request, "hoodmap.html", {"people": people, "buildings": buildings, "raw_buildings": raw_buildings.values(), "raw_people": raw_people.values()})


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
