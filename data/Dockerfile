FROM postgres:16-alpine
EXPOSE 5432
COPY init.sql /docker-entrypoint-initdb.d/
RUN rm -rf /var/lib/postgresql/data