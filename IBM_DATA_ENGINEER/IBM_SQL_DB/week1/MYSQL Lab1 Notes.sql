-- MY SQL Notes
-- connect to mysql cli and run the following:

mysql> CREATE DATABASE <db_name>;
mysql> USE  <db_name>;

-- get the script: world_mysql_script.sql
-- wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DB0231EN-SkillsNetwork/datasets/World/world_mysql_script.sql
-- and run it
mysql> SOURCE world_mysql_script.sql;

-- show the tables crated
mysql> SHOW TABLES;

-- show the ENGINES
-- default is InnoDB
mysql> SHOW ENGINES;
mysql> SHOW ENGINES;
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| Engine             | Support | Comment                                                        | Transactions | XA   | Savepoints |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+
| FEDERATED          | NO      | Federated MySQL storage engine                                 | NULL         | NULL | NULL       |
| MEMORY             | YES     | Hash based, stored in memory, useful for temporary tables      | NO           | NO   | NO         |
| InnoDB             | DEFAULT | Supports transactions, row-level locking, and foreign keys     | YES          | YES  | YES        |
| PERFORMANCE_SCHEMA | YES     | Performance Schema                                             | NO           | NO   | NO         |
| MyISAM             | YES     | MyISAM storage engine                                          | NO           | NO   | NO         |
| MRG_MYISAM         | YES     | Collection of identical MyISAM tables                          | NO           | NO   | NO         |
| BLACKHOLE          | YES     | /dev/null storage engine (anything you write to it disappears) | NO           | NO   | NO         |
| CSV                | YES     | CSV storage engine                                             | NO           | NO   | NO         |
| ARCHIVE            | YES     | Archive storage engine                                         | NO           | NO   | NO         |
+--------------------+---------+----------------------------------------------------------------+--------------+------+------------+

-- create a table using a csv engine (two columns: "i", int and "c" chars)
-- insert some data
mysql> CREATE TABLE csv_test (i INT NOT NULL, c CHAR(10) NOT NULL) ENGINE = CSV;
mysql> INSERT INTO csv_test VALUES(1,'data one'),(2,'data two'),(2,'data three');

-- MYSQL HAS SYSTEM DB/TABLES
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| information_schema |  -- <-- has (rad Only) metadata about the names of schema/db and the type of columns etc..
| mysql              |  -- <-- system table
| performance_schema |
| sys                |
| world              | -- <-- db created before
+--------------------+
--
--
mysql> USE mysql;
mysql> SHOW TABLES;
+----------------------------------------------+
| Tables_in_mysql                              |
+----------------------------------------------+
| columns_priv                                 |
| component                                    |
| db                                           |
...
...

| time_zone_transition                         |
| time_zone_transition_type                    |
| user                                         |
+----------------------------------------------+
34 rows in set 
--
-- example:
mysql> SELECT User from user;
+------------------+
| User             |
+------------------+
| root             |
| mysql.infoschema |
| mysql.session    |
| mysql.sys        |
| root             |
+------------------+
5 rows in set (0.00 sec)
--
--
mysql> USE information_schema;
mysql> SHOW TABLES;
mysql> show tables;
+---------------------------------------+
| Tables_in_information_schema          |
+---------------------------------------+
| ADMINISTRABLE_ROLE_AUTHORIZATIONS     |
| APPLICABLE_ROLES                      |
| CHARACTER_SETS                        |
| CHECK_CONSTRAINTS                     |
| COLLATIONS                            |
| COLLATION_CHARACTER_SET_APPLICABILITY |
| COLUMNS                               |
...
...
| VIEWS                                 |
| VIEW_ROUTINE_USAGE                    |
| VIEW_TABLE_USAGE                      |
+---------------------------------------+
79 rows in set (0.00 sec)

mysql> SELECT COLUMN_NAME FROM COLUMNS WHERE TABLE_NAME = 'country';
+----------------+
| COLUMN_NAME    |
+----------------+
| Code           |
| Name           |
| Continent      |
| Region         |

-- some interesting info like 
-- Table engine
-- table size
-- table schema
SELECT table_name, engine , (data_length + index_length)/1024 , table_schema
FROM INFORMATION_SCHEMA.TABLES 
WHERE table_name in ( 'country','city','countrylanguage','csv_test' );