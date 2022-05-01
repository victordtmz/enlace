SELECT 
  id, 
  name_ AS "Name",
  mc AS "MC",
  usdot AS "USDOT",
  phone AS "Phone",
  address AS "Address",
  address1 AS "Address",
  city as "City",
  state AS "State",
  zip AS "Zip",
  notes AS "Notes",
  invoiceEmail AS "Invoice Email",
  invoiceNotes AS "Invoice Notes"
  FROM clients
  ORDER BY 
  name_
  ;