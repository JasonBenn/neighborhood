CREATE MATERIALIZED VIEW houses_aggregated AS
select zn.apn,
       zn.geometry,
       zn.zone,
       tx.year_property_built,
       ow.year_built,
       tx.number_of_bedrooms,
       zl.bedrooms,
       tx.number_of_rooms,
       tx.number_of_bathrooms,
       tx.number_of_units,
       tx.property_area,
       ow.total_sqft,
       zl.sqft,
       tx.use_code,
       tx.property_class_code,
       ow.ot_sale_date,
       ow.market_sale_date,
       ow.prior_sale_date,
       zl.price_history,
       zl.zillow_url,
       zl.time_scraped,
       zl.label
from houses_neighborhoodbuildings zn
         left join houses_taxassessordata tx on zn.apn = tx.apn
         left join houses_owners ow on zn.apn = ow.apn
         left join houses_zillowdata zl on zn.apn = zl.apn;


DROP MATERIALIZED VIEW houses_aggregated;

REFRESH MATERIALIZED VIEW houses_aggregated;


-- Create assessor_use_codes mapping
CREATE MATERIALIZED VIEW assessor_use_codes as
(
select distinct use_code, use_definition
from houses_assessorclasscodes
    );

-- Most recent profile for each Zillow scraped_address.
CREATE MATERIALIZED VIEW zillow_addresses as (
select distinct on (scraped_address) *
from houses_zillowsnapshot
order by scraped_address, time_scraped desc
);

DROP MATERIALIZED VIEW zillow_addresses;