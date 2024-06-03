create database ep2_1;
create database ep2_2;
create database ep2_3;

\c ep2_2
CREATE EXTENSION postgis;
create extension postgres_fdw;
CREATE EXTENSION IF NOT EXISTS intarray;
create schema ep2_2_schema;
create table ep2_2_schema.original(id serial,
    idejemplar varchar, 
    numcatalogo varchar, 
    numcolecta varchar, 
    coleccion varchar, 
    institucion varchar, 
    fechacolecta varchar, 
    aniocolecta float, 
    calificadordeterminacion varchar, 
    procedenciaejemplar varchar, 
    ejemplarfosil boolean, 
    obsusoinfo varchar, 
    formadecitar varchar, 
    licenciauso varchar, 
    proyecto varchar, 
    urlorigen varchar, 
    ultimafechaactualizacion varchar, 
    "version" varchar, 
    familia varchar, 
    genero varchar, 
    especie varchar, 
    categoriainfraespecie varchar, 
    categoriainfraespecie2 varchar, 
    reinovalido varchar, 
    phylumdivisionvalido varchar, 
    clasevalida varchar, 
    ordenvalido varchar, 
    familiavalida varchar, 
    generovalido varchar, 
    especievalida varchar, 
    categoriainfraespecievalida varchar, 
    categoriainfraespecie2valida varchar, 
    autorvalido varchar, 
    grupobio varchar, 
    subgrupobio varchar, 
    cites varchar, 
    iucn varchar, 
    nom059 varchar, 
    prioritaria varchar, 
    nivelprioridad varchar, 
    exoticainvasora varchar, 
    endemismo varchar, 
    longitud float, 
    latitud float, 
    paisoriginal varchar, 
    paismapa varchar, 
    estadooriginal varchar, 
    estadomapa varchar, 
    municipiooriginal varchar, 
    municipiomapa varchar, 
    localidad varchar, 
    anp varchar, 
    altitudmapa float, 
    regionmarinamapa varchar, 
    incertidumbreXY float, 
    geoportal boolean);
CREATE INDEX idx_original_id ON ep2_2_schema.original(id);
ALTER TABLE ep2_2_schema.original ADD COLUMN the_geom geometry;

create table ep2_2_schema.variable(id serial, "values" json);
CREATE INDEX idx_variable_id ON ep2_2_schema.variable(id);

create table ep2_2_schema.occurrence_ensemble_ind(cell_id bigint, variable_id bigint);
CREATE INDEX idx_occurrence_ensemble_ind_cell_id ON ep2_2_schema.occurrence_ensemble_ind(cell_id);
CREATE INDEX idx_occurrence_ensemble_ind_variable_id ON ep2_2_schema.occurrence_ensemble_ind(variable_id);

create table ep2_2_schema.occurrence_ensemble_16k(cell_id bigint, variable_id bigint);
CREATE INDEX idx_occurrence_ensemble_16k_cell_id ON ep2_2_schema.occurrence_ensemble_16k(cell_id);
CREATE INDEX idx_occurrence_ensemble_16k_variable_id ON ep2_2_schema.occurrence_ensemble_16k(variable_id);

create table ep2_2_schema.summary_ensemble_ind(variable_id bigint, cells integer[], occs integer);
CREATE INDEX idx_summary_ensemble_ind_variable_id ON ep2_2_schema.summary_ensemble_ind(variable_id);

create table ep2_2_schema.summary_ensemble_16k(variable_id bigint, cells integer[], occs integer);
CREATE INDEX idx_summary_ensemble_16k_variable_id ON ep2_2_schema.summary_ensemble_16k(variable_id);

\c ep2_1
create extension postgres_fdw;
CREATE EXTENSION IF NOT EXISTS intarray;
CREATE SERVER ep2_2_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '127.0.0.1', dbname 'ep2_2', port '5433');
CREATE USER MAPPING FOR postgres SERVER ep2_2_server OPTIONS (user 'postgres', password 'postgres');
create schema ep2_2_schema;
IMPORT FOREIGN SCHEMA ep2_2_schema FROM SERVER ep2_2_server INTO ep2_2_schema;
CREATE SERVER ep2_3_server FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host '127.0.0.1', dbname 'ep2_3', port '5433');
CREATE USER MAPPING FOR postgres SERVER ep2_3_server OPTIONS (user 'postgres', password 'postgres');
create schema ep2_3_schema;


--CREATE FOREIGN TABLE test_table_2 (id serial, att_2 varchar(20)) SERVER ep2_2_server;
--CREATE FOREIGN TABLE test_table_3 (id serial, att_3 varchar(20)) SERVER ep2_3_server;