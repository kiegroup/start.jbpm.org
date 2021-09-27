# USED AS REFERENCE ONLY
# run from parent dir:
# docker build --tag  registry.access.redhat.com/ubi8/openjdk-8:latest -f jbpm-bootstrap-service/src/main/docker/openshift.Dockerfile .
FROM  registry.access.redhat.com/ubi8/openjdk-8:latest

USER jboss

ENV JAVA_OPTIONS "-Dorg.kie.version=7.RELEASE -Dspring.profiles.active=openshift -Dkie.maven.settings.custom=/opt/jboss/.m2/settings.xml"

RUN mkdir -p /opt/jboss/.m2/repository

COPY --chown=jboss jbpm-bootstrap-service/target/*.jar /deployments
COPY --chown=jboss jbpm-bootstrap-service/bootstrap-jbpm.xml /deployments
COPY --chown=jboss jbpm-bootstrap-service/src/main/docker/settings.xml /opt/jboss/.m2
COPY --chown=jboss jbpm-bootstrap-kjar/target/local-repository/maven /opt/jboss/.m2/repository

