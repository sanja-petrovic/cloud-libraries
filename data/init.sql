SELECT 'CREATE DATABASE central_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'central_db')\gexec
SELECT 'CREATE DATABASE ns_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ns_db')\gexec
SELECT 'CREATE DATABASE nis_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'nis_db')\gexec
SELECT 'CREATE DATABASE bg_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'bg_db')\gexec
