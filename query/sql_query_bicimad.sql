SELECT 
bs.name AS "BiciMAD station",
bs.address AS "Station location",
bs."geometry.coordinates" AS "Coordinates"
FROM
bicimad.main.bicimad_stations  AS bs;