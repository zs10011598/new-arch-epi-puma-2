# new-arch-epi-puma-2

Este es un demo de la propuesta de nueva arquitectura de Epi-PUMA 2.0

# description

Esta nueva propuesta, en escencia es, una base de datos federada con un solo gateway ep2_1 y que es capaz de hacer queries a las bases de datos (nodos) ep2_2 y ep2_3.

* En la base de datos ep2_1 es para poner tablas generales para todos los nodos, como por ejemplo las geometrías de las mallas espaciales. 
* En este demo la base de datos ep2_2 contiene el SNIB con las tablas necesarias para los ensambles de individuos y de celdas (regular 16km).
* En el nodo ep2_3 es casi identica a la ep2_2, solo cambie el nombre del esquema para probar con distintos queries desde el gateway ep2_1.
* En ambos nodos (ep2_2 y ep2_3) hay una tabla de variables que funciona tanto para el ensamble de individuos como el de celdas.

# run

Este es el orden en el que se tienen que correr los archivos

    - Crear las bases de datos con el scrip sql `init_db.sql`
    - Asegurarse de que exista el directorio `species_data` y que contenga un archivo `.zip` del SNIB, descargar de https://snib.mx/.
    - Correr notebook de Jupyter `build_db.ipynb` o `build_db.py`.
    - Crear la base de datos `ep2_3` copiando `ep2_2`, en la consola interactiva de `PostgreSQL`, tecleado `CREATE DATABASE ep2_3 FROM TEMPLATE ep2_2`.
    - Conectarse a la base de datos `ep2_3` con el comando `\c ep2_3`.
    - Renombrar el esquema con `ALTER SCHEMA ep2_2_schema RENAME TO ep2_3_schema`.
    - Conectarse a la base de datos `ep2_1`.
    - Importar el esquema `ep2_3_schema` con el comando `IMPORT FOREIGN SCHEMA ep2_3_schema FROM SERVER ep2_3_server INTO ep2_3_schema;`.
    - Correr las celdas del notebook de Jupyter `compute_analysis.ipynb`.

# developer

- Pedro R [pedro.romero@c3.unam.mx]