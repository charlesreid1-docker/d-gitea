# d-gitea

This is the gitea docker container used to run gitea on charlesreid1.com.

You should not run this container by itself (see 
[pod-charlesreid1](https://git.charlesreid1.com/docker/pod-charlesreid1.git)). 

See the documentation here: <https://pages.charlesreid1.com/d-gitea/>

## TODO

Organize the documentation better, there's a lot going on

* Setup
* Repo organization
* Jinja/ansible
* Gitea files
* New instance
* Restoring instance
* Backing up instance

## Quick Start

### Before you begin

Check `docker-compose.yml` and ensure the bind mounting of folders is
set up to match what you want. Currently:

* `d-gitea/custom/` directory maps to `/data/gitea` in the container
* `d-gitea/data/` directory maps to `/app/gitea/data`

To change this, modify the `docker-compose.yml` file in this repo
or the `docker-compose.yml.j2` file in the pod-charlesreid1 repo.

### Create app.ini

The `app.ini` file is not stored directly in this repo, only a template file
`app.ini.j2` is stored. You need to create an `app.ini` file from the template
before beginning.

To create an `app.ini` file from the template, populate the secret files at:

* `internal_token.secret`
* `secret_key.secret`

Then run the `make_app_ini.sh` script:

```
./make_app_ini.sh
```

This will create an `app.ini` file from the template at `custom/conf/app.ini.j2`,
and will put the new file in `custom/conf/app.ini`.

### Running

Start the container with `docker-compose up` if running standalone, or by starting
the docker pod if running in a pod.

## Links

[documentation: d-gitea container](https://pages.charlesreid1.com/d-gitea/)

[source code on git.charlesreid1.com: docker/d-gitea](https://git.charlesreid1.com/docker/d-gitea)

[source code on github.com: charlesreid1-docker/d-gitea](https://github.com/charlesreid1-docker/d-gitea) (you are here)

[gitea documentation - running gitea with docker](https://docs.gitea.io/en-us/install-with-docker/)

