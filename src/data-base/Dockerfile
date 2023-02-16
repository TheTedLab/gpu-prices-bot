FROM postgres:14-alpine3.14
COPY create_tables.sql /docker-entrypoint-initdb.d/
ENV POSTGRES_PASSWORD=video_cards_data_user
ENV POSTGRES_HOST_AUTH_METHOD=trust
