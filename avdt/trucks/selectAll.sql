SELECT 
  trucks.id, 
  carriers.name_ AS "Carrier",
  no_ AS "No",
  vin AS "VIN",
  year_ AS "Year",
  make AS "Make",
  model AS "Model",
  trucks.notes AS "Notes"
  FROM trucks
  LEFT JOIN carriers ON carriers.id = trucks.idCarrier
  ORDER BY no_
  ;