SELECT 
  id, 
  name_ AS "Name",
  mc AS "MC",
  usdot AS "USDOT",
  ein AS "EIN",
  agent AS "Agent",
  phone AS "Phone",
  address AS "Address",
  address1 AS "Address",
  zip AS "Zip",
  city as "City",
  state AS "State",
  notes AS "Notes"
  FROM carriers
  ORDER BY 
  name_
  ;