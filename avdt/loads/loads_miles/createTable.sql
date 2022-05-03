CREATE TABLE miles_loads (
    id INT NOT NULL AUTO_INCREMENT,
    idLoad INT,
    idMiles INT,
    no_ CHAR(5),
    date_ DATE,
    PRIMARY KEY (id),
    FOREIGN KEY (idLoad) REFERENCES loads(id),
    FOREIGN KEY (idMiles) REFERENCES miles(id)
    )
ENGINE = InnoDB;

-- DROP TABLE miles_loads;