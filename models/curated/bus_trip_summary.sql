MODEL (
 name bus_trip_db.bus_trip_summary,
 kind INCREMENTAL_BY_TIME_RANGE (
 time_column year_month
 ),
);

SELECT
 year_month,
 bus_region,
 card_type,
 SUM(trips) AS total_trips
FROM bus_trip_db.raw_bus_trip_counts_filtered
WHERE trips > 1
GROUP BY
 year_month,
 bus_region,
 card_type