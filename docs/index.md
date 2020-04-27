# d-gitea

Docker files for running gitea

[documentation: d-gitea container](https://pages.charlesreid1.com/d-gitea/) (you are here)

[source code on git.charlesreid1.com: d-gitea](https://git.charlesreid1.com/docker/d-gitea)

[source code on github.com: charlesreid1-docker/d-gitea](https://github.com/charlesreid1-docker/d-gitea)

[gitea documentation - running gitea with docker](https://docs.gitea.io/en-us/install-with-docker/)


## Table of Contents

* secrets
* jinja templates
* container directory structure
* container data volume
* files mounted into container
* using the `docker-compose.yml` file
* notes on custom files
* configuring gitea with `app.ini`
* customizing gitea with custom files
* backing up and restoring gitea

## Secrets

There are two secrets to set in the `app.ini` before running gitea:
the internal token and the secret key.

These can be set in `*.secret` files:

```plain
internal_token.secret
secret_key.secret
```

The contents should be the value of the variable 
you wish to use in `custom/conf/app.ini`.

These files are not tracked by git.

## Jinja Templates

The `app.ini` script is not stored directly in this repo, since it contains
sensitive information. Instead, we store a Jinja template, `app.ini.j2`, which
is rendered into a real `app.ini` file after variable substitutions, etc.

Normally, we use this repo with Ansible, so we don't deal with the Jinja template
ourselves.

If you want to render the Jinja template into a real config file without using
Ansible, use the `make_app_ini.sh` script:

```
$ ./make_app_ini.sh
```

(This requires the two secret files mentioned above to be present.)

## Container Directory Structure

The `custom/` dir in this folder maps to the `/data/gitea` volume
inside the gitea container.

For example, the `app.ini` configuration file will be mapped into 
the container at `/data/gitea/conf/app.ini`.

## Container Data Volume

This container expects to use a docker data volume 
to store the gitea custom configuration 
and the entire contents of all repositories.

On the host machine, you can access named data volumes at 
`/var/lib/docker/volumes/gitea_gitea/_data`
or copy files in and out of the container using `docker cp`.

### directory structure before adding repos to gitea

Directory structure for host-mounted gitea directory
before any repositories have been added to gitea:

```plain
gitea
├── git
│   └── repositories
├── gitea
│   ├── conf
│   │   └── app.ini
│   ├── gitea.db
│   ├── indexers
│   │   └── issues.bleve
│   │       ├── index_meta.json
│   │       └── store
│   ├── lfs
│   ├── log
│   │   ├── gitea.log
│   │   ├── http.log
│   │   └── xorm.log
│   └── sessions
│       └── oauth2
└── ssh [error opening dir]

11 directories, 7 files
```

### directory structure after adding repos to gitea

After adding a repository:

```plain
gitea
├── git
│   └── repositories
│       └─e charlesreid1
│           └── oieruoweiur.git
│               ├── branches
│               ├── config
│               ├── description
│               ├── HEAD
│               ├── hooks
│               │   ├── applypatch-msg.sample
│               │   ├── commit-msg.sample
│               │   ├── post-receive
│               │   ├── post-receive.d
│               │   │   └── gitea
│               │   ├── post-update.sample
│               │   ├── pre-applypatch.sample
│               │   ├── pre-commit.sample
│               │   ├── prepare-commit-msg.sample
│               │   ├── pre-push.sample
│               │   ├── pre-rebase.sample
│               │   ├── pre-receive
│               │   ├── pre-receive.d
│               │   │   └── gitea
│               │   ├── pre-receive.sample
│               │   ├── update
│               │   ├── update.d
│               │   │   └── gitea
│               │   └── update.sample
│               ├── info
│               │   ├── exclude
│               │   └── refs
│               ├── objects
│               │   ├── info
│               │   │   └── packs
│               │   └── pack
│               └── refs
│                   ├── heads
│                   └── tags
├── gitea
│   ├── conf
│   │   └── app.ini
│   ├── gitea.db
│   ├── indexers
│   │   └── issues.bleve
│   │       ├── index_meta.json
│   │       └── store
│   ├── lfs
│   ├── log
│   │   ├── gitea.log
│   │   ├── http.log
│   │   └── xorm.log
│   └── sessions
│       └── oauth2
└── ssh [error opening dir]

25 directories, 29 files
```

## Files Mounted Into Container

The `d-gitea/custom/` directory is mounted into the container at `/data/gitea`.

The `d-gitea/data/` directory is mounted into the container at `/app/gitea/data`.

To make the custom configuration file, follow the instructions mentioned in
the "Secrets" section.



## Using the `docker-compose.yml` File

### Standalone

This directory contains a docker-compose file that can be used to run 
a gitea server on port 3000.

To get the gitea container up and running, 

```plain
$ docker-compose up
```

Now visit `<server-ip>:3000`. You will be presented with a configuration page.
Set up the gitea instance. This will automatically populate the directory 
structure. See below for more info.

Use this as a project seed to add gitea containers to other docker pods.

### pod-charlesreid1

The main use of this repo is as a submodule in
[pod-charlesreid1](https://github.com/charlesreid1-docker/pod-charlesreid1.git).

This pod is set up by Ansible, which integrates well with the Jinja template approach.

## Notes on Custom Files

The settings in the `app.ini` file are documented [here](https://docs.gitea.io/en-us/config-cheat-sheet/).

An extensive sample `app.ini` file is [here](https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample) (WARNING: this broke gitea).

The existing gitea templates are in the gitea repo under [templates/](https://github.com/go-gitea/gitea/tree/master/templates).
These can be modified as needed and placed in the `custom/templates/` directory.

### custom templates directory

The templates directory `d-gitea/custom/templates` contains template files. 
These are gitea templates that control how particular kinds of gitea pages look.
For example, a template can be used to modify how the user page looks, or modify
the layout of repository main pages.

In the container, this will be at `/data/gitea/templates/`.

### custom gitea pages

The custom pages directory `d-gitea/custom/pages` contains one-off pages or static
content that is hosted by the gitea instance, but not necessarily incorporated into
the gitea site.

For example, a custom "about me" page could be added as a static .html file,
and it would be hosted at `git.charlesreid1.com/about`.

In the container, this will be at `/data/gitea/pages/`.


## Backing up and restoring gitea

Running `gitea dump` command will dump files required for restoring an existing
Gitea instance. Unfortunately, gitea's backup and restore functionality is an
absolute dumpster fire.

We do our best to walk through the process, but here is a summary:
* On the old system:
    * Create a backup file `gitea-dump.zip` using the very specific `gitea dump` incantation that works
    * Move the backup file out of the gitea container
* On the new system:
    * Unzip the backup file `gitea-dump.zip`
    * Put appropriate files in appropriate location
    * Use the table below to determine where in the repo the gitea dump files should go,
      and where they will be available inside the gitea container

### Creating a Backup

To create a gitea dump, connect to the docker container and get a bash shell as the user
`git` via the docker exec command:

```
# connect to gitea container
docker exec -it --user git name_of_gitea_container /bin/bash
```

This will give you a bash shell as the user `git`. Now create a gitea dump file
(the gitea dump command requires you to be in `/app/gitea`, this assumes that the
gitea executable is at the default location of `/app/gitea/gitea`):

```
# necessary
cd /app/gitea
# create gitea dump
/app/gitea/gitea dump --file gitea-dump.zip --skip-repository
```

**IMPORTANT: The `--skip-repositories` flag means we are making the gitea dump
way, way, way smaller, but it also means we need to back up and restore the
repositories folder ourselves! (See below for instructions.)**

Now copy the file out of the container, then remove it from the container:

```
# copy gitea dump out of container
docker cp name_of_gitea_container:/app/gitea/gitea-dump.zip .

# remove gitea dump
docker exec -it name_of_gitea_container rm /app/gitea/gitea-dump.zip
```

### Contents of Dump File

When the gitea dump file is unzipped, it will create the following files:

* `app.ini`
* `custom/` directory
* `log/` directory (useless duplicate, already contained in `custom/` dir)
* `data/` directory

These files should map to the following locations in the docker container
running the live gitea instance:

```
gitea dump file:        gitea live instance:
----------------        --------------------
app.ini                 /data/gitea/conf/app.ini
custom/                 /data/gitea/
log/                    (useless duplicate of custom/log/)
data                    /app/gitea/data
```

### Restoring a Backup

To restore a backup, copy the following files from the gitea dump
to the following locations inside this repository:

```
gitea dump file:        d-gitea repo location:
----------------        ----------------------
app.ini                 d-gitea/custom/conf/app.ini
custom/*                d-gitea/custom/*
data                    d-gitea/data
```

(If you're running pod-charlesreid1, put these files in the
specified location in the `d-gitea` submodule.)

### Restoring repositories directory

Note that when we created the gitea dump, we excluded the repositories themselves.
This is because these will greatly inflate the size of our gitea dump and will make
it much more difficult to store our backup files.

Repository contents can be backed up separately as follows:

* Log in to the old server
* Back up the `/data/git/repositories` directory (copy and compress)
* Copy the backup to the new server
* Log in to the new server
* Mount the `/data/git/repositories` folder

Optionally, if you want to keep the repositories folder in its own location,
modify `docker-compose.yml` to add the following line to the `gitea` container's
`volumes` configuration:

```
services:
  server:
    image: gitea/gitea:latest

    ...

    volumes:
      - "/path/to/repositories:/data/git/repositories"
    
    ...
```

This should make it easier to manage, back up, and restore the repositories folder.

### Database backups

We opt for the SQLite backend for gitea, which means the database
is kept in a flat file on disk called `/data/gitea/gitea.db`.

The location of this file and the format of the database are specified
in the config file in `d-gitea/custom/conf/app.ini`.

This file should not be edited, instead change the Jinja template
`d-gitea/custom/conf/app.ini.j2` and remake `app.ini` from the template.

