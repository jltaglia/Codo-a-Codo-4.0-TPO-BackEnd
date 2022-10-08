LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/categorias.csv' 
INTO TABLE categorias 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/est_civil.csv' 
INTO TABLE est_civil 
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/eventos.csv' 
INTO TABLE eventos
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/parentescos.csv' 
INTO TABLE parentescos
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/provincias.csv' 
INTO TABLE provincias
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/tipo_doc.csv' 
INTO TABLE tipo_doc
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/personal.csv' 
INTO TABLE personal
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/Users/jltag/Mi unidad/2 - IT/Codo a Codo 2022 - FullStack Python/TPO Back/Varios/csv/localidades_reduc.csv' 
INTO TABLE localidades
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;