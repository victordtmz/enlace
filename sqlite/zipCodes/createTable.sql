CREATE TABLE IF NOT EXISTS zipCodes (
    zip TEXT NOT NULL PRIMARY KEY,
    stateName TEXT,
    stateId TEXT,
    city TEXT,
    county TEXT,
    lat REAL,
    lng REAL
    )