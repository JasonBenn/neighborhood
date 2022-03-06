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

select count(*) from houses_aggregated;
select count(*) from houses_aggregated where houses_aggregated.zillow_url is not null;
select apn from houses_zillowdata where zillow_url is not null;
select count(*) from houses_aggregated where price_history is not null;