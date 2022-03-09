import json
from uuid import UUID

from django.http import HttpResponse
from django.shortcuts import render

from houses.models import Rater, Rating

next_listings_sql = """
select z.id, substring(z.address from '^(.*), San Francisco') as address, z.bedrooms, z.baths, z.sqft, count(r.id) as num_ratings, min(r.value) as min_rating, z.zillow_url, z.filenames
from houses_zillowsnapshot z
left join houses_rating r on z.id = r.zillow_snapshot_id
where jsonb_array_length(z.filenames) > 3
group by z.id
having (count(r.id) = 0) or (count(r.id) = 1 and min(r.value) > 5) or (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
order by random()
limit 1;
"""

leaderboard_sql = """
select rater.name, count(all_ratings) num_ratings, round(avg(all_ratings.value - ground_truth), 1) calibration
from houses_rater rater
join houses_rating all_ratings on all_ratings.rater_id = rater.id
join houses_zillowsnapshot z on all_ratings.zillow_snapshot_id = z.id
left join (select z.id, avg(rating.value) as ground_truth
      from houses_rating rating
           join houses_rater rater on rating.rater_id = rater.id
           join houses_zillowsnapshot z on rating.zillow_snapshot_id = z.id
      group by z.id
      having count(rating.value) > 1
) as ground_truths on ground_truths.id = z.id
group by rater.id
order by count(all_ratings) desc;
"""


def index(request):
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute(next_listings_sql)
    next_listings = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    listings = [dict(zip(colnames, x)) for x in next_listings]
    listings = [{**x, **{
        'filenames': json.loads(x['filenames'])
    }} for x in listings]

    cursor.execute(leaderboard_sql)
    raw_leaderboard = cursor.fetchall()
    leaderboard = [{
        "name": x[0],
        "num_ratings": x[1],
        "calibration": x[2]
    } for x in raw_leaderboard]

    raters = Rater.objects.all()

    return render(request, "ratings.html", {
        "listings": listings,
        "raters": raters,
        "leaderboard": leaderboard,
        "active_rater_id": request.session.get('active_rater_id'),
        "is_leaderboard_hidden": request.session.get('is_leaderboard_hidden')
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
    request.session['is_leaderboard_hidden'] = bool(data['isLeaderboardHidden'])
    print(request.session['is_leaderboard_hidden'])
    return HttpResponse(status=204)
