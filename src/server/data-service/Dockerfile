FROM gradle:jdk17
WORKDIR /data-service
COPY build.gradle .
COPY ./src ./src
ENTRYPOINT ["gradle", "run"]