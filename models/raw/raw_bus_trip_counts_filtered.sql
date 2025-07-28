MODEL (
 name bus_trip_db.raw_bus_trip_counts_filtered,
 kind FULL,
);

SELECT
 year_month,
 bus_region,
 card_type,
 trips
FROM iceberg.bus_trip_db.raw_bus_trip_counts
WHERE trips > 1;