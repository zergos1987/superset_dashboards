create database dashbaords;
create database superset;
create schema user_dashboards; -- on database dashbaords;

create role "postgres_dashboards" WITH LOGIN PASSWORD 'some_password';


GRANT USAGE, CREATE ON SCHEMA "db_dashboards" TO "postgres_dashboards";
GRANT SELECT, INSERT, UPDATE, DELETE, TRUNCATE ON ALL TABLES IN SCHEMA "db_dashboards" TO "postgres_dashboards";
ALTER DEFAULT PRIVILEGES IN SCHEMA "db_dashboards" GRANT SELECT, INSERT, UPDATE, CREATE, DELETE, TRUNCATE ON TABLES TO "postgres_dashboards";

-- ----------------------------------

SELECT usename AS role_name,
 CASE
  WHEN usesuper AND usecreatedb THEN
    CAST('superuser, create database' AS pg_catalog.text)
  WHEN usesuper THEN
    CAST('superuser' AS pg_catalog.text)
  WHEN usecreatedb THEN
    CAST('create database' AS pg_catalog.text)
  ELSE
    CAST('' AS pg_catalog.text)
 END role_attributes
FROM pg_catalog.pg_user
ORDER BY role_name desc;

select *
from information_schema.role_table_grants 
where table_schema = 'db_dashboards' 
--where grantee = 'postgres_dashboards'
