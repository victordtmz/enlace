SELECT 
  loads.id, 
  contracting.name_ AS "Contractin",
  hauling.name_ AS "Hauling",
  trucks.no_ AS "Truck",
  trailers.no_ AS "Trailer",
  drivers.name_ AS "Driver",
  loads.contractDate AS "Date",
  clients.name_ AS "Client",
  agents.name_ AS "Clients Agent",
  loads.referenceNo AS "Reference",
  loads.rate AS "Rate",
  loads.dateInvoice AS "Invoice Date",
  loads.amountPaid AS "Amount Paid",
  loads.datePaid AS "Date Paid",
  loads.notes AS "Notes",
  loads.delivered AS "Delivered",
  loads.invoiced AS "invoiced",
  loads.paid AS "Paid",
  loads.paidHCarrier AS "Paid H Carrier",
  loads.completed AS "Completed"
  FROM loads
  LEFT JOIN carriers contracting ON contracting.id = loads.idContracting
  LEFT JOIN carriers hauling ON hauling.id = loads.idHauling
  LEFT JOIN trucks ON trucks.id = loads.idTruck
  LEFT JOIN trailers ON trailers.id = loads.idTrailer
  LEFT JOIN drivers ON drivers.id = loads.idDriver
  LEFT JOIN clients ON clients.id = loads.idClient
  LEFT JOIN clients_agents agents ON agents.id = loads.idClientAgent
  ORDER BY loads.contractDate DESC
  ;