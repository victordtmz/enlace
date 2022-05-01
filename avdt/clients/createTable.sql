CREATE TABLE clients (
    id INT NOT NULL AUTO_INCREMENT,
    name_ VARCHAR(255),
    mc CHAR(7),
    usdot CHAR(8),
    phone CHAR(10),
    address VARCHAR(255),
    address1 VARCHAR(255),
    city VARCHAR(255),
    state CHAR(2),
    zip CHAR(5),
    notes TEXT,
    invoiceEmail VARCHAR(255),
    invoiceNotes TEXT,
    PRIMARY KEY (id)
    )
ENGINE = InnoDB;