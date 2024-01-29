-- get the DB data from here:
-- wget https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/example-guided-project/flights_RUSSIA_small.sql

-- restore the file downloaded into the pgadmin console session
\i flights_RUSSIA_small.sql

-- check the tables
demo-# \dt
               List of relations
  Schema  |      Name       | Type  |  Owner   
----------+-----------------+-------+----------
 bookings | aircrafts_data  | table | postgres
 bookings | airports_data   | table | postgres
 bookings | boarding_passes | table | postgres
 bookings | bookings        | table | postgres
 ...

 -- A PostgreSQL server instance has a corresponding file named postgresql.conf 
 -- See postgres > data > postgresql.conf
 -- that contains the configuration parameters for the server. By modifying this file, 
 -- you can enable, disable, or otherwise customize the settings of your PostgreSQL server 
 -- instance to best suit your needs as a database administrator. 
 -- While you can manually modify this postgresql.conf file and restart the server for the changes to take effect, 
 -- you can also edit some configuration parameters directly from the command line interface (CLI).

-- this shows the level of the write-ahead log (WAL)
-- see https://www.postgresql.org/docs/9.6/runtime-config-wal.html
# SHOW wal_level;
 wal_level 
-----------
 replica
(1 row)

-- you can change it with:
ALTER SYSTEM SET wal_level = 'logical';
-- however hte change will only take effect if you restart the service..
-- the command above creates a new file: postgres.auto.conf in postgres > data > postgresql.auto.conf.
-- with this content (note that the -- are not in the file):
--
-- # Do not edit this file manually!
-- # It will be overwritten by the ALTER SYSTEM command.
-- wal_level = 'logical'
--
--
-- YOU can check the list of databases:
# \l
or 
# SELECT datname FROM pg_database; 

-- you can see the tables in a schema with:
SELECT * FROM pg_tables WHERE schemaname = '<schema_name>';

-- you can also see al settings;
-- or specific settings (with where conditions)
SELECT name, setting, short_desc FROM pg_settings -- WHERE name = 'wal_level';

-- even if these are system tables you can actively modify them (but don't.. it's dangerous)
-- example, change a table name in a schema
UPDATE pg_tables SET tablename = '<new_name>' WHERE tablename = '<old_name>';
UPDATE pg_tables SET tablename = 'aircraft_fleet' WHERE tablename = 'aircrafts_data';