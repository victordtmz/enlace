CREATE TABLE bookkeeping_diesel (
    id INT NOT NULL,
    gallons DECIMAL(13,4),
    jurisdiction VARCHAR(2),
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES bookkeeping(id)
    )
ENGINE = InnoDB;

-- DROP TABLE bookkeeping_diesel;