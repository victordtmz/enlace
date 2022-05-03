CREATE TABLE miles_locations (
    id INT NOT NULL,
    location_ VARCHAR(255),
    isBorder TINYINT(1),
    border_ CHAR(5),
    PRIMARY KEY (id)
    )
ENGINE = InnoDB;