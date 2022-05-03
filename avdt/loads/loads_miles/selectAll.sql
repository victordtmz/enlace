SELECT 
  drivers.id, 
  carriers.name_ AS "Carrier",
  drivers.name_ AS "Name",
  dob AS "Date of Birth",
  drivers.phone AS "Phone",
  drivers.address AS "Address",
  drivers.address1 AS "Address",
  drivers.city as "City",
  drivers.state AS "State",
  drivers.zip AS "Zip",
  licNo AS "No. Licencia", 
  licIss AS "Expedicion",
  licExp AS "Vencimiento",
  licState AS "Estado",
  drivers.notes AS "Notes"
  FROM drivers
  LEFT JOIN carriers ON carriers.id = drivers.idCarrier
  ORDER BY drivers.name_
  ;