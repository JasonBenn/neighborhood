select count(*)
from houses_neighborhoodbuildings as n
         join houses_taxassessordata as t on n.apn = t.apn;


select count(*)
from (
         select distinct apn
         from houses_owners
     ) as o;

select count(o.apn)
from houses_neighborhoodbuildings as n
         join houses_owners as o on n.apn = o.apn;

select count(*)
from (select distinct o.apn
      from houses_neighborhoodbuildings as n
               left join houses_addresses as o on n.apn = o.apn) as foo;

select apn, site_address
from houses_owners
where houses_owners.apn not in
      (select o.apn
       from houses_neighborhoodbuildings as n
                join houses_owners as o on n.apn = o.apn
      )
  and apn like '%53%'
order by apn;

select apn
from houses_neighborhoodbuildings
where houses_neighborhoodbuildings.apn like '%537%'
order by apn;

select apn
from houses_neighborhoodbuildings
where houses_neighborhoodbuildings.apn not in
      (select o.property_id
       from houses_neighborhoodbuildings as n
                join houses_owners as o on n.apn = o.apn
      );

-- How well did the materialized table join together?
-- Compare counts of non-nullable columns from each source table
-- neighborhoodbuildings: 5340
select count(*)
from houses_aggregated;
-- owners
select count(*)
from houses_aggregated
where houses_aggregated.ot_sale_date is not null;
select count(*)
from houses_aggregated
where houses_aggregated.market_sale_date is not null;
select count(*)
from houses_aggregated
where houses_aggregated.prior_sale_date is not null;

-- tax assessor data

-- zillow data

select count(*)
from houses_aggregated
where houses_aggregated.zillow_url is not null;
select count(*)
from houses_aggregated
where houses_aggregated.time_scraped is not null;
select count(*)
from houses_aggregated
where price_history is not null;
select count(*)
from houses_aggregated
where houses_aggregated.geometry is not null;

select count(*)
from (select hn.apn, count(ad.address) cnt
      from houses_addresses ad
               join houses_neighborhoodbuildings hn on ad.apn = hn.apn
      group by hn.apn
      having count(ad.address) <= 4) cnt;

select ad.apn, ad.address
from houses_addresses ad
         join houses_neighborhoodbuildings hn on ad.apn = hn.apn
where ad.address like '%PAGE ST'
order by ad.address;

COPY (
    select addrs.apn, addrs.address, cnts.cnt, cnts.geom
    from houses_addresses addrs
             join
         (select ad.apn, count(ad.address) cnt, max(geometry) geom
          from houses_addresses ad
                   join houses_neighborhoodbuildings hn on ad.apn = hn.apn
          group by ad.apn) as cnts on cnts.apn = addrs.apn
    where addrs.address like '%PAGE ST'
      and (addrs.address like '23%' or addrs.address like '22%')
    order by addrs.address
    ) TO '/Users/jasonbenn/Desktop/page_st_test.csv' (format csv);


-- This one exports all buildings
COPY (
    select addrs.apn, address, unit_number, zip_code, geometry
    from houses_addresses addrs
             join houses_neighborhoodbuildings hn on addrs.apn = hn.apn
--     where addrs.address like '%PAGE ST'
--       and (addrs.address like '23%' or addrs.address like '22%'or addrs.address like '24%')
    order by addrs.address
    ) TO '/Users/jasonbenn/Desktop/page_st_test.csv' (format csv);


-- list all buildings
COPY (
    select addrs.apn, concat(addrs.address, ', San Francisco, CA ', addrs.zip_code) address
    from houses_addresses addrs
             join houses_taxassessordata tx on addrs.apn = tx.apn
             join houses_neighborhoodbuildings b on addrs.apn = b.apn
             join
         (select ad.apn, count(ad.address) cnt
          from houses_addresses ad
                   join houses_neighborhoodbuildings hn on ad.apn = hn.apn
          group by ad.apn
          having count(ad.address) <= 4) cnts on cnts.apn = addrs.apn
    order by zone, addrs.apn, addrs.address
    ) TO '/Users/jasonbenn/Desktop/2022-03-07_all_addresses.csv' (format csv);

-- search compound APNs
copy (
    select addrs.apn,
           concat(min(addrs.address_number), '-', max(addrs.address_number), ' ', min(addrs.street_name), ' ',
                  min(addrs.street_type), ', San Francisco, CA ',
                  min(addrs.zip_code)) address --, use_code, property_class_code
    from houses_addresses addrs
             join houses_neighborhoodbuildings hn on addrs.apn = hn.apn
             left join houses_taxassessordata tx on addrs.apn = tx.apn
    group by zone, addrs.apn
    having count(addrs.address) > 1
    order by zone, addrs.apn, address
    ) TO '/Users/jasonbenn/Desktop/2022-03-07_all_addresses_compound.csv' (format csv);

SELECT column_name
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name = 'houses_zillowdata';


select least('301 a', '306');

select addrs.apn, address, unit_number, zip_code
from houses_addresses addrs
where addrs.address like '1095%'
--       and unit_number is not null
order by addrs.address

-- select 1 random record that has...
--   0 records
--   1 record, if rated gt 5
--   2 records, if diff b/w them is >= 2
select z.id,
       substring(z.address from '^(.*), San Francisco') as address,
       z.bedrooms,
       z.baths,
       z.sqft,
       count(r.id)                                      as num_ratings,
       min(r.value)                                     as min_rating,
       z.zillow_url,
       z.filenames,
       z.price_history
from houses_zillowsnapshot z
         left join houses_rating r on z.id = r.zillow_snapshot_id
where jsonb_array_length(z.filenames) > 3
group by z.id
having (count(r.id) = 1 and min(r.value) > 5)
    or (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
order by random()
limit 10;
-- (count(r.id) = 0)


select z.id,
       substring(z.address from '^(.*), San Francisco') as address,
       z.bedrooms,
       z.baths,
       z.sqft,
       count(r.id)                                      as num_ratings,
       min(r.value)                                     as min_rating,
       z.zillow_url,
       z.filenames
from houses_zillowsnapshot z
         left join houses_rating r on z.id = r.zillow_snapshot_id
where jsonb_array_length(z.filenames) > 3
group by z.id
having (count(r.id) = 0)
    or (count(r.id) = 1 and min(r.value) > 5)
    or (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
order by random()
limit 10;

-- leaderboard, with calibration
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


-- progress query
-- number of ratings w:
--   0 ratings
--   1 rating lte 5
--   1 record, gt 5
--   2 records, diff lte 2
--   2 records, diff gt 2
--   3 ratings
-- algo estimates total number of needed ratings:
--   need 1
--   need 2:
--   need 3: 2 records, diff gt 2, 3 ratings

-- start with number of listings that have > 3 images
select rating_counts.listing_ratings as num_ratings, rating_counts.count
from (
         select count(rating) listing_ratings
         from houses_zillowsnapshot z
                  left join houses_rating rating on z.id = rating.zillow_snapshot_id
         where jsonb_array_length(z.filenames) > 3
         group by z.id
     ) as rating_counts
group by rating_counts.listing_ratings
order by num_ratings;

select count(*)
from houses_rating;

select min(rating.created)
from houses_rating as rating
group by rating.zillow_snapshot_id;

-- num single-rated that need another rating
select count(*)
from (
         select rating.zillow_snapshot_id, min(rating.created) first_created
         from houses_rating as rating
         group by rating.zillow_snapshot_id
         having count(*) = 1
     ) as single_rated
join houses_rating rating on rating.zillow_snapshot_id = single_rated.zillow_snapshot_id and rating.created = single_rated.first_created
where rating.value > 5;

-- num double-rated that need a 3rd rating
select count(*)
from (
         select rating.zillow_snapshot_id, min(rating.created) first_created
         from houses_rating as rating
         group by rating.zillow_snapshot_id
         having count(*) = 1
     ) as single_rated
join houses_rating rating on rating.zillow_snapshot_id = single_rated.zillow_snapshot_id and rating.created = single_rated.first_created
where rating.value > 5;

-- double rated, need a 3rd
select r.zillow_snapshot_id, count(r.id), max(r.value), min(r.value)
from houses_rating r
group by r.zillow_snapshot_id
having (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2);
