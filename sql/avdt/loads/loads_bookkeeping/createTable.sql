CREATE TABLE bookkeeping_loads (
    idBookkeeping INT NOT NULL,
    idLoads INT NOT NULL,
    PRIMARY KEY (idBookkeeping, idLoads),
    FOREIGN KEY (idBookkeeping) REFERENCES bookkeeping(id),
    FOREIGN KEY (idLoads) REFERENCES loads(id)
    )
ENGINE = InnoDB;