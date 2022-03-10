NUM_HOUSES_BY_TYPE = """
select use_definition, count(*) count
from houses_neighborhoodbuildings
         join houses_taxassessordata tx on houses_neighborhoodbuildings.apn = tx.apn
         join assessor_use_codes ha on tx.use_code = ha.use_code
group by use_definition
order by count desc;
"""

NUM_HOUSES_BY_TYPE = """
select *
from houses_neighborhoodbuildings
         join houses_taxassessordata tx on houses_neighborhoodbuildings.apn = tx.apn
         join assessor_use_codes ha on tx.use_code = ha.use_code;
"""

LEADERBOARD = """
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
NEXT_LISTINGS = """
select z.id, substring(z.address from '^(.*), San Francisco') as address, z.bedrooms, z.baths, z.sqft, count(r.id) as num_ratings, min(r.value) as min_rating, z.zillow_url, z.filenames
from houses_zillowsnapshot z
left join houses_rating r on z.id = r.zillow_snapshot_id
where jsonb_array_length(z.filenames) > 3
group by z.id
having (count(r.id) = 0) or (count(r.id) = 1 and min(r.value) > 5) or (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
order by random()
limit 1;
"""