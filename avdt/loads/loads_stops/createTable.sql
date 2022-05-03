CREATE TABLE loads_stops (
    id INT NOT NULL AUTO_INCREMENT,
    idLoad INT,
    idStop INT,
    type_ TINYINT(1),
    no_ INT,
    appointment DATETIME,
    po VARCHAR(255),
    notes TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (idLoad) REFERENCES loads(id),
    FOREIGN KEY (idStop) REFERENCES stops(id)
    )
ENGINE = InnoDB;