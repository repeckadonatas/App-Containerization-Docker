DO
$do$
BEGIN
   IF EXISTS (SELECT FROM pg_database WHERE datname = 'kaggle-data-db') THEN
      RAISE NOTICE 'Database already exists';  -- optional
   ELSE
      PERFORM dblink_exec('dbname=' || current_database()  -- current db
                        , 'CREATE DATABASE kaggle-data-db');
   END IF;
END
$do$;