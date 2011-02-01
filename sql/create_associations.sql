CREATE TABLE IF NOT EXISTS associations (
    code TEXT NOT NULL PRIMARY KEY,
    name TEXT DEFAULT NULL
);

INSERT INTO associations VALUES ('cus', 'Centro Universitario Sportivo');
INSERT INTO associations VALUES ('a', 'Atleta UISP');
INSERT INTO associations VALUES ('g', 'Giovani UISP');
INSERT INTO associations VALUES ('d', 'Dirigente UISP');
INSERT INTO associations VALUES ('sa', 'Scheda attività UISP');
INSERT INTO associations VALUES ('e', 'Estiva UISP');
