# start.jbpm.org Website

Official repository of the [start.jbpm.org](https://start.jbpm.org) website.

To try the website locally, just run:

```shell
./launch.sh clean install
```

This command will build the application and the website image.

After some time, access the application via [http://localhost:8090/](http://localhost:8090/).

## Building the Website

**IMPORTANT!** First thing you need to do is run a complete `mvn clean install` from the main 
module (this project's root) to create the local maven repository.

All the commands below must be run inside the module [`jbpm-bootstrap-service`](jbpm-bootstrap-service).

### Docker profile

In this profile, just a regular docker image is built with the website in order to try it locally.
To build using this profile, run the following command:

````shell
## remember to run inside jbpm-bootstrap-service
$ mvn clean install -Pdocker
````

An image named `jbpm/jbpm-bootstrap-service:latest` will be available in your local registry.

Run it with:

```shell
$ docker run --rm -it -p 8090:8090 jbpm/jbpm-bootstrap-service:latest
```

### OpenShift Online

This profile builds an image that exposes the secure `8443` port to be deployed on OpenShift online:

```
## remember to run inside jbpm-bootstrap-service
$ mvn clean install -Popenshift
```

A valid certificate for the domain start.jbpm.org named `keystore.p12` must be placed on 
[`src/main/resources`](jbpm-bootstrap-service/src/main/resources) folder in order to make this work.

Run it with:

```shell
$ docker run --rm -it -p 8443:8443 jbpm/jbpm-bootstrap-service:latest
```

### OpenShift Managed

For OpenShift Managed, the profile `openshift_internal` should be used.
This profile exposes the service on port `8090` and creates all Kubernetes objects necessary
to deploy the application on a managed Kubernetes or OpenShift cluster. It also works on Minikube.

The service can be exposed via an OpenShift Route or a Kubernetes Ingress by the administrator.

To build it, run the following command:

```shell
## remember to run inside jbpm-bootstrap-service
$ mvn clean install -Popenshift_internal
```

The image should be available in your local docker registry.

Alternatively, if you're testing on minikube run `eval $(minikube docker-env)` before executing the `mvn` command.
This way, the image will be built directly to your minikube registry.

Use the following command to deploy the application on a Kubernetes/OpenShift cluster:

```shell
$ kubectl apply -f jbpm-bootstrap-service/target/classes/META-INF/jkube/kubernetes.yml -n <namespace>
```

This command will deploy a ConfigMap, a Service, a Deployment, and a PVC in the given namespace.

#### Exposing the service on Minikube

Simply run:

````shell
$ minikube service --url jbpm-bootstrap-service -n <namespace>
````

This will expose the created service as a NodePort in your machine. 
The first address is the endpoint for the application.

### Bump Versions

There are two places to update as soon as a new version is released: the version mapping configuration file and the projects POM.

#### Updating the Configuration File

All the versions used in the website interface are in the [`application.yml`](jbpm-bootstrap-service/src/main/resources/application.yml)
file. Just add the next versions to this file.

On OpenShift, this file is mounted as a `ConfigMap`. All you have to do is to update this file with the new version.

On OpenShift Online, the file is being read from the classpath, so the image must be built again and pushed to the cluster
after updating the file.

#### Updating the application POM file

This project is a jBPM application, thus it uses the latest released version. 
Just update it in the POM files from the [kjar](jbpm-bootstrap-kjar/pom.xml) and [service](jbpm-bootstrap-service/pom.xml) 
projects as part of the bump process of all the modules of the KIE Group projects.

#### Finding the correct version

For community, you can take a look at the [JBoss Repository](https://repository.jboss.org/nexus/index.html#nexus-search;gav~org.jbpm~jbpm-workitems~~~).

On Enterprise, check the equivalent version in this [Support Article](https://access.redhat.com/articles/3463751).
