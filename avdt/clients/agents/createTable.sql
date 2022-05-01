CREATE TABLE clients_agents (
    id INT NOT NULL,
    idClient INT,
    name_ VARCHAR(255),
    phone CHAR(10),
    ext VARCHAR(10),
    email VARCHAR(255),
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (idClient) REFERENCES clients(id)
    )
ENGINE = InnoDB;