SELECT 
  trailers.id, 
  carriers.name_ AS "Carrier",
  no_ AS "No",
  vin AS "VIN",
  year_ AS "Year",
  make AS "Make",
  model AS "Model",
  trailers.notes AS "Notes"
  FROM trailers
  LEFT JOIN carriers ON carriers.id = trailers.idCarrier
  ORDER BY no_
  ;