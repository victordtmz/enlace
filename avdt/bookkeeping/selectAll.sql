SELECT
-- DISPLAY VALUES
bookkeeping.id AS "ID",
bookkeeping.date_ AS "Date",
CONCAT("$", FORMAT(bookkeeping.amount,2)) as "Amount", 

bookkeeping.description_ AS "Description",

-- HIDDEN VALUES
bookkeeping.idCarrier AS "4-Carrier",
-- bookkeeping.idCategorie AS "5-Categorie",
bookkeeping.anexo AS "5-Anexo",

-- FILTER VALUES
-- YEAR(bookkeeping.date_) AS "6-Year",
DATE_FORMAT(bookkeeping.date_, '%m') AS "7-Month",
categories.categorie "8-Categorie",
CASE WHEN bookkeeping.isBusiness = 1 THEN "True" ELSE "False" END as "9- IsBusiness",
bookkeeping.account_ AS "10-Account",
CASE WHEN bookkeeping.isIncome = 1 THEN "Income" ELSE "Expense" END as "11-Type"
-- u210833393_AVD.AVDT_Carriers.name_ AS "13-Carrier",
-- Main Table 
FROM bookkeeping
-- Join Statements
LEFT JOIN bookkeeping_categories categories ON  categories.id = bookkeeping.idCategorie
-- Where condition statements
WHERE bookkeeping.idCarrier = %s
AND YEAR(bookkeeping.date_) LIKE %s
;