SELECT 
  agents.id, 
  clients.name_ AS "Client",
  agents.name_ AS "Agent",
  agents.phone AS "Phone",
  agents.ext AS "Extention",
  agents.email AS "Email",
  agents.notes AS "Notes"
  FROM clients_agents agents
  LEFT JOIN clients ON clients.id = agents.idClient
  ORDER BY agents.name_
  ;