NUM_HOUSES_BY_TYPE = """
select use_definition, count(*) count
from houses_neighborhoodbuildings
         join houses_taxassessordata tx on houses_neighborhoodbuildings.apn = tx.apn
         join assessor_use_codes ha on tx.use_code = ha.use_code
group by use_definition
order by count desc;
"""

LEADERBOARD = """
select rater.name, count(all_ratings) num_ratings, round(avg(all_ratings.value - ground_truth), 1) calibration
from houses_rater rater
join houses_rating all_ratings on all_ratings.rater_id = rater.id
join zillow_addresses z on all_ratings.zillow_snapshot_id = z.id
left join (select z.id, avg(rating.value) as ground_truth
      from houses_rating rating
           join houses_rater rater on rating.rater_id = rater.id
           join zillow_addresses z on rating.zillow_snapshot_id = z.id
      group by z.id
      having count(rating.value) > 1
) as ground_truths on ground_truths.id = z.id
group by rater.id
order by count(all_ratings) desc;
"""

NEXT_LISTINGS = """
select z.id, substring(z.address from '^(.*), San Francisco') as address, z.bedrooms, z.baths, z.sqft, r.num_ratings, r.min_rating, z.zillow_url, z.filenames
from zillow_addresses z
left join (
    select zil.id, count(rs.id) as num_ratings, min(rs.value) as min_rating, max(rs.value) as max_rating
    from zillow_addresses zil
        left join houses_rating rs on zil.id = rs.zillow_snapshot_id
    group by zil.id
    ) as r on r.id = z.id
where jsonb_array_length(z.filenames) > 3
and (r.num_ratings = 0) or (r.num_ratings = 1 and r.min_rating > 5) or (r.num_ratings = 2 and (r.max_rating - r.min_rating) >= 2)
order by random()
limit 1;
"""

NEEDS_FIRST_RATING_COUNT = """
select count(*)
from (
         select count(rating) listing_ratings
         from zillow_addresses z
                  left join houses_rating rating on z.id = rating.zillow_snapshot_id
         where jsonb_array_length(z.filenames) > 3
         group by z.id
         having count(rating) = 0
     ) zero_rated;"""

NEEDS_SECOND_RATING_COUNT = """
select count(*) count_single_rated
from (
         select rating.zillow_snapshot_id, min(rating.created) first_created
         from houses_rating as rating
         group by rating.zillow_snapshot_id
         having count(*) = 1
     ) as single_rated
         join houses_rating rating on rating.zillow_snapshot_id = single_rated.zillow_snapshot_id and
                                      rating.created = single_rated.first_created
where rating.value > 5;"""

NEEDS_THIRD_RATING_COUNT = """
select count(*)
from (
         select r.zillow_snapshot_id, count(r.id), max(r.value), min(r.value)
         from houses_rating r
         group by r.zillow_snapshot_id
         having (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
     ) double_rated;"""

COUNT_RATINGS = """
select count(*)
from houses_rating;"""
