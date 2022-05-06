CREATE TABLE carriers_clients (
    id INT NOT NULL AUTO_INCREMENT,
    carrier INT,
    client INT,
    date_ DATE,
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (carrier) REFERENCES carriers(id),
    FOREIGN KEY (client) REFERENCES clients(id)
    )
ENGINE = InnoDB;