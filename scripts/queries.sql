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
from zillow_addresses z
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
from zillow_addresses z
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

-- One rater's ratings vs ground truths
select round(avg(all_ratings.value - ground_truth), 1)
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
where rater.name = 'Loewen'
group by all_ratings.zillow_snapshot_id
order by count(all_ratings) desc;

select min(created), max(created)
from houses_rating;


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
EXPLAIN ANALYZE
select rating_counts.listing_ratings as num_ratings, rating_counts.count
from (
         select count(rating) listing_ratings
         from zillow_addresses z
                  left join houses_rating rating on z.id = rating.zillow_snapshot_id
         where jsonb_array_length(z.filenames) > 3
         group by z.id
     ) as rating_counts
group by rating_counts.listing_ratings
order by num_ratings;

select value rating_value, count(*) num_ratings
from houses_rating
group by value
order by rating_value;

select count(*)
from houses_rating;

select min(rating.created)
from houses_rating as rating
group by rating.zillow_snapshot_id;

-- zero-counted ratings
select count(*)
from (
         select count(rating) listing_ratings
         from zillow_addresses z
                  left join houses_rating rating on z.id = rating.zillow_snapshot_id
         where jsonb_array_length(z.filenames) > 3
         group by z.id
         having count(rating) = 0
     ) zero_rated;

-- num single-rated that need another rating
EXPLAIN ANALYZE
select count(*) count_single_rated
from (
         select rating.zillow_snapshot_id, min(rating.created) first_created
         from houses_rating as rating
         group by rating.zillow_snapshot_id
         having count(*) = 1
     ) as single_rated
         join houses_rating rating on rating.zillow_snapshot_id = single_rated.zillow_snapshot_id and
                                      rating.created = single_rated.first_created
where rating.value > 5;

-- double rated, need a 3rd
EXPLAIN ANALYZE
select count(*)
from (
         select r.zillow_snapshot_id, count(r.id), max(r.value), min(r.value)
         from houses_rating r
         group by r.zillow_snapshot_id
         having (count(r.id) = 2 and (max(r.value) - min(r.value)) >= 2)
     ) double_rated;

-- non-compound addrs stats
select houses.apn,
       rating_counts.scraped_address,
       bedrooms,
       sqft,
       jsonb_array_length(price_history) / 4,
       jsonb_array_length(filenames)
from houses_neighborhoodbuildings houses
         left join zillow_addresses zil on houses.apn = zil.apn
         left join (
    select scraped_address, count(ratings.id)
    from houses_rating ratings
             join zillow_addresses hz on ratings.zillow_snapshot_id = hz.id
    group by scraped_address
) as rating_counts on zil.scraped_address = rating_counts.scraped_address
where rating_counts.scraped_address not like '%-%'
order by houses.apn, zil.address;

-- compound addrs vs not by housing type
select use_code, scraped_address like '%-%' as compound_addr, count(houses.apn) count
from houses_neighborhoodbuildings houses
         left join zillow_addresses zil on houses.apn = zil.apn
         left join houses_taxassessordata ht on zil.apn = ht.apn
group by use_code, compound_addr
order by count desc;


select rating.*
from houses_rating rating;

-- validating that Zillow scraped_addresses are actually getting the newest snapshot...
select time_scraped, scraped_address
from zillow_addresses
where scraped_address = '712-714 Masonic Ave, San Francisco, CA 94117';
select scraped_address, count(scraped_address) as times_scraped, min(time_scraped), max(time_scraped)
from houses_zillowsnapshot
group by scraped_address
having count(scraped_address) > 1;


-- Original, mysteriously working query
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
limit 5;

-- revised to work with zillow_addresses
select z.id,
       substring(z.address from '^(.*), San Francisco') as address,
       z.bedrooms,
       z.baths,
       z.sqft,
       r.num_ratings,
       r.min_rating,
       z.zillow_url,
       z.filenames
from zillow_addresses z
         left join (
    select zil.id, count(rs.id) as num_ratings, min(rs.value) as min_rating
    from zillow_addresses zil
             join houses_rating rs on zil.id = rs.zillow_snapshot_id
    group by zil.id
) as r on r.id = z.id
;

-- Pricing histories
select *, jsonb_array_length(price_history) / 4 len_history
from zillow_addresses
where jsonb_array_length(price_history) / 4 > 1;

-- Price histories, NOO
select *, jsonb_array_length(price_history) / 4 len_history
from zillow_addresses
         left join houses_owners ho on zillow_addresses.apn = ho.apn
where mailing_address != site_address
  and jsonb_array_length(price_history) / 4 > 1;

-- Price histories, OO
select zil.apn,
       scraped_address,
       zestimate,
       price_history,
       bool(mailing_address = site_address) owner_occupied,
       bedrooms,
       sqft,
       sqft / bedrooms                      sqft_per_br
from zillow_addresses zil
         left join houses_owners ho on zil.apn = ho.apn
    and jsonb_array_length(price_history) / 4 > 1;

-- Delete
delete
from houses_zillowsnapshot;

-- Alter a foreign key constraint to ON DELETE SET NULL
ALTER TABLE houses_rating
    DROP CONSTRAINT houses_rating_zillow_snapshot_id_9400d6d5_fk_houses_zi;

ALTER TABLE houses_rating
    ADD CONSTRAINT houses_rating_zillow_snapshot_id_9400d6d5_fk_houses_zi
        FOREIGN KEY (zillow_snapshot_id) REFERENCES houses_zillowsnapshot
            ON DELETE SET NULL;

-- DDL:
--     zillow_snapshot_id     uuid
--         constraint houses_rating_zillow_snapshot_id_9400d6d5_fk_houses_zi
--             references houses_zillowsnapshot
--             deferrable initially deferred,

--     zillow_snapshot_id     uuid
--         constraint houses_rating_zillow_snapshot_id_9400d6d5_fk_houses_zi
--             references houses_zillowsnapshot
--             on delete set null,

select count(*)
from houses_zillowsnapshot;

select count(*)
from zillow_addresses;

update houses_rating rating
set zillow_snapshot_id = (
    select id
    from zillow_addresses add
    where rating.zillow_scraped_address = add.scraped_address
);

-- Number of houses to rate
select count(*)
from zillow_addresses z
where jsonb_array_length(z.filenames) > 3;

-- select count(*) 3,667 - is that how many we made? Yes.

select hz.apn,
       avg(rat.value)                 avg_rating,
       geometry,
       scraped_address,
       scraped_address is not null as found_on_zillow
from houses_rating rat
         join houses_zillowsnapshot hz on rat.zillow_snapshot_id = hz.id
         full join houses_neighborhoodbuildings hn on hz.apn = hn.apn
group by hz.apn, geometry, scraped_address;

-- where rat.value = 10;

COPY (
         SELECT row_to_json(fc)
FROM (SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features
      FROM (SELECT 'Feature'                       As type
                 , ST_AsGeoJSON(lg.geometry)::json As geometry
                 , row_to_json(lp)                 As properties
            FROM houses_neighborhoodbuildings As lg
                     INNER JOIN (
                select hn.id,
                       hz.apn,
                       avg(rat.value)                 avg_rating,
                       geometry,
                       scraped_address,
                       scraped_address is not null as found_on_zillow
                from houses_rating rat
                         join houses_zillowsnapshot hz on rat.zillow_snapshot_id = hz.id
                         full join houses_neighborhoodbuildings hn on hz.apn = hn.apn
                group by hn.id, hz.apn, geometry, scraped_address
            ) As lp
                                ON lg.id = lp.id) As f) As fc
    ) TO '/Users/jasonbenn/Desktop/data/buildings.geojson';


select bedrooms, count(*) from zillow_addresses
group by bedrooms
order by bedrooms;

select distinct count(apn) from houses_neighborhoodbuildings;

-- MRES >= 4BR: 1026 / (1250 + 1026) * (1250 + 1026 + 4070) = 2861
-- SRES >= 4BR: 392 / (392 + 1244) * (1244 + 393 + 606) = 537

-- MRES >= 6BR: 396 / (1880 + 396) * (1880 + 396 + 4070) = 1104
-- SRES >= 6BR: 65 / (65 + 1571) * (1571 + 393 + 606) = 102
select use_code, bedrooms >= 6 as ">= 6BR", count(*) from houses_neighborhoodbuildings
join houses_addresses ha on houses_neighborhoodbuildings.apn = ha.apn
join houses_taxassessordata ht on houses_neighborhoodbuildings.apn = ht.apn
join zillow_addresses za on ha.apn = za.apn
where use_code in ('SRES', 'MRES')
group by use_code, bedrooms >= 6
order by use_code, bedrooms >= 6;

select use_code, count(*) from houses_neighborhoodbuildings
join houses_addresses ha on houses_neighborhoodbuildings.apn = ha.apn
join houses_taxassessordata ht on houses_neighborhoodbuildings.apn = ht.apn
join zillow_addresses za on ha.apn = za.apn
where use_code in ('SRES', 'MRES')
group by use_code
order by use_code;

-- MRES NOO: 5585 / (727 + 5585) * (5585 + 727 + 1877) = 7246
-- SRES NOO: 128 / (128 + 282) * (128 + 282 + 1905) = 723
-- NOO: 5441 + 697 = 6138
-- Total residential units: 5585 + 727 + 1877 + 128 + 282 + 1905 = 10504
-- Total buildings: 5340
-- (Might be double-counting buildings bc Neighbohood buildings divides them by area)
select use_code, mailing_address = site_address, bedrooms, count(*) from houses_neighborhoodbuildings
left join houses_addresses ha on houses_neighborhoodbuildings.apn = ha.apn
join houses_taxassessordata ht on houses_neighborhoodbuildings.apn = ht.apn
left join zillow_addresses za on ha.apn = za.apn
left join houses_owners ho on ha.apn = ho.apn
where use_code in ('SRES', 'MRES')
group by use_code, mailing_address = site_address, bedrooms
order by use_code, mailing_address = site_address;


-- 1: 243
-- 2: 631
-- 3: 619
-- 4: 368
-- 5: 174
-- 6: 103