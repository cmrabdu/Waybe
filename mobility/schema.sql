DROP TABLE IF EXISTS ville;
CREATE TABLE IF NOT EXISTS ville (
    code_postal INTEGER NOT NULL PRIMARY KEY,
    nom TEXT NOT NULL,
    population INTEGER NOT NULL
);

DROP TABLE IF EXISTS rue;
CREATE TABLE IF NOT EXISTS rue (
    rue_id INTEGER NOT NULL PRIMARY KEY,
    nom TEXT NOT NULL,
    code_postal INTEGER NOT NULL,
    FOREIGN KEY (code_postal) REFERENCES ville(code_postal)
);

DROP TABLE IF EXISTS vitesse;
CREATE TABLE IF NOT EXISTS vitesse (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    tranche_de_vitesse INTEGER NOT NULL,
    proportion REAL NOT NULL,
    PRIMARY KEY (rue_id, tranche_de_vitesse, date),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);

DROP TABLE IF EXISTS v85;
CREATE TABLE IF NOT EXISTS v85 (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    v85 REAL,
    PRIMARY KEY (rue_id, date),
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id)
);

DROP TABLE IF EXISTS traffic;
CREATE TABLE IF NOT EXISTS traffic (
    rue_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    type_vehicule TEXT NOT NULL,
    nb_vehicules INTEGER NOT NULL,
    FOREIGN KEY (rue_id) REFERENCES rue(rue_id),
    PRIMARY KEY (rue_id, type_vehicule, date)
);