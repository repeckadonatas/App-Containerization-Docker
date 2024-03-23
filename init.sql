CREATE ROLE root;
ALTER ROLE root WITH LOGIN;
CREATE DATABASE "root";
CREATE DATABASE "kaggle-data-db";

-- CREATE EXTENSION IF NOT EXISTS dblink;
--
-- DO
-- $do$
-- BEGIN
--    IF EXISTS (SELECT FROM pg_database WHERE datname = 'kaggle-data-db') THEN
--       RAISE NOTICE 'Database already exists';
--    ELSE
--       PERFORM dblink_exec('dbname=' || current_database()
--                         , 'CREATE DATABASE "kaggle-data-db"');
--    END IF;
-- END
-- $do$;