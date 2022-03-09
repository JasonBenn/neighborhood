import json
from pprint import pprint
from uuid import UUID

from django.http import HttpResponse
from django.shortcuts import render

from houses.models import Rater, Rating


def index(request):
    from django.db import connection
    raw_query = """select z.id, substring(z.address from '^(.*), San Francisco') as address, z.bedrooms, z.baths, z.sqft, count(r.id) as num_ratings, min(r.value) as min_rating, z.zillow_url, z.filenames
    from houses_zillowsnapshot z
    left join houses_rating r on z.id = r.zillow_snapshot_id
    where jsonb_array_length(z.filenames) > 3
    group by z.id
    having (count(r.id) = 0) or (count(r.id) = 1 and min(r.value) > 5) or (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
    order by random()
    limit 1;
    """

    cursor = connection.cursor()
    cursor.execute(raw_query)
    results = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    zillow_listings = [dict(zip(colnames, x)) for x in results]
    zillow_listings = [{**x, **{
        'filenames': json.loads(x['filenames'])
    }} for x in zillow_listings]

    raters = Rater.objects.all()

    return render(request, "ratings.html", {
        "zillow_listings": zillow_listings,
        "raters": raters,
        "active_rater_id": request.session.get('active_rater_id')
    })


def create_rating(request):
    data = json.loads(request.body)
    rater_id = int(data['raterId'])
    Rating.objects.create(
        rater_id=rater_id,
        zillow_snapshot_id=UUID(data['zillowSnapshotId']),
        value=int(data['value']) if data['value'] else None,
    )
    request.session['active_rater_id'] = rater_id
    return HttpResponse(status=204)
