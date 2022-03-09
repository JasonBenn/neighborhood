from pprint import pprint

from django.shortcuts import render

from houses.models import Rater


def index(request):
    from django.db import connection
    raw_query = """select z.id, substring(z.address from '^(.*), San Francisco') as address, z.bedrooms, z.baths, z.sqft, z.zillow_url, z.filenames, count(r.id), min(r.label)
    from houses_zillowsnapshot z
    left join houses_rating r on z.id = r.zillow_snapshot_id
    where z.filenames is not null
    group by z.id
    order by random()
    limit 1;
    """

    cursor = connection.cursor()
    cursor.execute(raw_query)
    results = cursor.fetchall()
    colnames = [desc[0] for desc in cursor.description]
    zillow_listings = [dict(zip(colnames, x)) for x in results]
    pprint(zillow_listings)

    raters = Rater.objects.all()

    return render(request, "ratings.html", {
        "zillow_listings": zillow_listings,
        "raters": raters,
        "active_rater_id": request.session.get('active_rater_id')
    })


# request.session['active_rater_id'] = rater_id