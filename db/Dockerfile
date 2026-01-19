FROM postgis/postgis:16-3.4

# Copy initialization scripts if they exist
COPY init-db.sql /docker-entrypoint-initdb.d/init-db.sql

# PostgreSQL will run on port 5432 by default
