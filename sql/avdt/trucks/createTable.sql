CREATE TABLE trucks (
    id INT NOT NULL,
    idCarrier INT,
    no_ VARCHAR(255),
    vin VARCHAR(255),
    year_ CHAR(4),
    make VARCHAR(255),
    model VARCHAR(255),
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (idCarrier) REFERENCES carriers(id)
    )
ENGINE = InnoDB;