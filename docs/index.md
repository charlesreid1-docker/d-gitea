# d-gitea

Docker files for running gitea

[documentation: d-gitea container](https://pages.charlesreid1.com/d-gitea/) (you are here)

[source code on git.charlesreid1.com: d-gitea](https://git.charlesreid1.com/docker/d-gitea)

[source code on github.com: charlesreid1-docker/d-gitea](https://github.com/charlesreid1-docker/d-gitea)

[gitea documentation - running gitea with docker](https://docs.gitea.io/en-us/install-with-docker/)


## Table of Contents

* secrets
* container directory structure
* files mounted into container
* using the `docker-compose.yml` file
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

### `custom/conf` configuration file

The conf dir contains configuration files to configure how gitea works.

The `app.ini` file needs to contain two secrets,
which are scrubbed in `app.ini.sample`.

The two secrets that are needed are:

* an "internal token" secret, contained in `internal_token.secret`
* a "secret key" secret, contained in `secret_key.secret`

Use the `make_app_ini.sh` script to add the two secrets to the document.
This will use sed to find/replace instances of the scrubbed secret,
and will output the result to `custom/conf/app.ini`.

```plain
./make_app_ini.sh
```

This generates `custom/conf/app.ini`.

When the container is run, this file will be at `/data/gitea/conf/app.ini`.

## `custom/templates` template files

The templates directory contains template files. These are gitea templates that 
control how particular kinds of gitea pages look. For example, a template can
be used to modify how the user page looks, or modify the layout of repository
main pages.

In the container, this will be at `/data/gitea/templates/`.

## `custom/pages` gitea pages

The pages directory contains one-off pages or static content that is 
hosted by gitea at the same domain (git.charlesreid1.com) but 
not necessarily incorporated into the gitea site.

For example, a custom "about me" page could be added as a static .html file,
and it would be hosted at `git.charlesreid1.com/about`.

In the container, this will be at `/data/gitea/pages/`.

## Using the `docker-compose.yml` File

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

## Notes on Custom Files

The settings in the app.ini file are documented [here](https://docs.gitea.io/en-us/config-cheat-sheet/).

An extensive sample app.ini file is [here](https://github.com/go-gitea/gitea/blob/master/custom/conf/app.ini.sample) (WARNING: this broke gitea).

The existing gitea templates are in the gitea repo under [templates/](https://github.com/go-gitea/gitea/tree/master/templates).
These can be modified as needed and placed in the `custom/templates/` directory.

## Backing Up and Restoring Gitea

Fortunately, gitea provides dump functionality.

Unfortunately, there is no restore functionality.

See [pod-charlesreid1/utils-gitea](https://git.charlesreid1.com/docker/pod-charlesreid1/src/branch/master/utils-gitea)
for proper backup/restore scripts.

### Executive Summary

Backup:

* create a backup target directory in the container
* create a gitea dump zip file using `gitea dump` command
* create a gitea avatars zip file
* copy everything in the backup target directory out of the container
* remove the backup target directory

Restore:

* create a restore target directory in the container
* copy gitea dump and gitea avatars zip files into restore target dir
* unpack dump zip, unpack avatars zip
* unzip repositories zip (contained in dump zip)
* restore `repositories/` folder to `/data/git/repositories/`
* (skip restoring `custom/` files, version control takes care of that)
* restore sqlite database using sql database dump
* restore avatars
* remove the restore target directory

