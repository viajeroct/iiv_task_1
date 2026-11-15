FROM gradle:8.10-jdk21 AS build
WORKDIR /src
COPY . .
RUN gradle bootJar --no-daemon
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/build/libs/app.jar app.jar
ENV IMPL=blocking
# IMPL=virtual включает виртуальные потоки; остальной код идентичен
CMD ["sh","-c","java -XX:MaxRAMPercentage=70 -Dspring.threads.virtual.enabled=$([ \"$IMPL\" = virtual ] && echo true || echo false) -jar app.jar"]
