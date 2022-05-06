CREATE TABLE bookkeeping (
    id INT NOT NULL,
    idCarrier INT,
    idCategorie INT,
    account_ VARCHAR(255),
    date_ DATE, 
    amount DECIMAL(13,2),
    isIncome TINYINT(1),
    description_ TEXT,
    anexo VARCHAR(255),
    isBusiness TINYINT(1),
    PRIMARY KEY (id),
    FOREIGN KEY (idCarrier) REFERENCES carriers(id),
    FOREIGN KEY (idCategorie) REFERENCES bookkeeping_categories(id)
    )
ENGINE = InnoDB;