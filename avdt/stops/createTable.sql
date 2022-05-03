CREATE TABLE stops (
    id INT NOT NULL,
    name_ VARCHAR(255),
    north VARCHAR(255),
    west VARCHAR(255),
    address_ VARCHAR(255),
    city VARCHAR(255),
    state_ CHAR(2),
    zip CHAR(5),
    phone CHAR(10),
    google VARCHAR(255),
    notes TEXT,
    PRIMARY KEY (id)
    )
ENGINE = InnoDB;
