# start.jbpm.org Website

Official repository of the [start.jbpm.org](https://start.jbpm.org) website.

To try the website locally, just run:

```shell
./launch.sh clean install -Popenshift
```

This command will build the application and the website image.

After some time, access the application via [http://localhost:8090/](http://localhost:8090/).

## CI/CD tooling

This repository also contains script and resources to automate [start.jbpm.org](https://start.jbpm.org) releases.

### Bump Versions

In order to bump versions from jBPM and/or Enterprise releases, clone the repositories `jbpm-bootstrap-model`, `jbpm-bootstrap-kjar` and `jbpm-bootstrap-service`:

```shell
$ ls
jbpm-bootstrap-kjar  jbpm-bootstrap-model  jbpm-bootstrap-service
```

In the parent directory run the following script:

```shell
$ python hack/bump-versions.py --community 7.45.0.Final --enterprise 7.9 --product 7.44.0.Final-redhat-00003
```

**Note:** Replace the given versions with the actual ones

The only required flag is **community**, since a product release is always followed up by a community release.

You can now prepare a PR for each project with the required version.

#### Finding the correct version

For community, you can take a look at the [JBoss Repository](https://repository.jboss.org/nexus/index.html#nexus-search;gav~org.jbpm~jbpm-workitems~~~).

On Enterprise, check the equivalent version in this [Support Article](https://access.redhat.com/articles/3463751).
