CREATE TABLE loads (
    id INT NOT NULL,
    idContracting INT,
    idHauling INT,
    idTruck INT, 
    idTruck INT, 
    idTruck INT, 
    idTruck INT, 
    idTruck INT, 
    
    name_ VARCHAR(255),
    dob DATE,
    phone CHAR(10),
    address VARCHAR(255),
    address1 VARCHAR(255),
    city VARCHAR(255),
    state CHAR(2),
    zip CHAR(5),
    licNo VARCHAR(255),
    licIss DATE,
    licExp DATE,
    licState VARCHAR(255),
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (idCarrier) REFERENCES carriers(id)
    )
ENGINE = InnoDB;