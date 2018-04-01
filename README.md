# d-gitea

Docker files for running gitea

[gitea with docker - documentation](https://docs.gitea.io/en-us/install-with-docker/)


## Table of Contents

* secrets
* container directory structure
* files mounted into container
* using the `docker-compose.yml` file
* configuring gitea with `app.ini`
* customizing gitea with custom files
* backing up and restoring gitea

## Secrets

There are two secrets to set in `app.ini` before running gitea:
the internal token and the secret key.

These can be set in `*.secret` files:

```
internal_token.secret
secret_key.secret
```

The contents should be the value of the variable 
you wish to use in `app.ini`.

These files are not tracked by git.

## Container Directory Structure

Any configuration of gitea will deposit files into `data/`.

Specifically, configuration file will be in `/data/gitea/conf/app.ini`.

On the host machine, you can access named data volumes at 
`/var/lib/docker/volumes/gitea_gitea/_data`
or using `docker cp`.

### directory structure before adding data

Directory structure for host-mounted gitea directory:

```
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

### directory structure after adding data

After adding data:

```
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

### app.ini

app.ini needs to be mounted into the container.

created app.ini here with two secrets scrubbed:

* an internal token secret contained in `internal_token.secret`
* a secret key secret contained in `secret_key.secret`

The `make_app_ini.sh` script will take the 
version-control-safe `api.sample` and use sed
to find and replace the secret keys with their values.

To run:

```
./make_app_ini.sh
```

which will generate `app.ini`, a file ignored by git.

The docker-compose file will automatically mount 
a file named `app.ini` in the current directory

### custom directory

The `custom/` directory should also be mounted in the container.
The custom directory contains templates and pages.

The docker-compose file will automatically mount the `custom/` directory.

## Using the `docker-compose.yml` File

to get this thing up and running:

```
$ docker-compose up
```

Now visit `<server-ip>:3000`. You will be presented with a configuration page.
Set up the gitea instance. This will automatically populate the directory 
structure. See below for more info.

## Configuring Gitea with `app.ini`

## Customizing Gitea with Custom Files

the main use of this container is part of the larger charlesreid1 pod,
so the main purpose of this repo is to store custom gitea files.

These are stored in `custom/`.

`custom/` should map to `/data/gitea/` inside the container.

## Backing Up and Restoring Gitea

Fortunately, gitea provides dump functionality.

Unfortunately, there is no restore functionality.

### gitea dump directory structure

The built-in `gitea dump` functionality will create a zip
that contains the following directory structure:

```
gitea-repo.zip
gitea-db.sql
custom/
log/
```

When the `gitea-repo.zip` folder is unzipped, it generates a `repositories/` folder
containing the contents of every git repo in the gitea site.

For the real gitea server, here is where these should go:

The `repositories/` dir should be at:

```
<gitea-base-dir>/repositories
```

The `custom/` dir should be at:

```
<gitea-base-dir>/bin/custom
```

The database file should be at:

```
<gitea-base-dir>/data/gitea-db.sql
```

The log should be at:

```
<gitea-base-dir>/log
```

### gitea dump and restore scripts

Our gitea backup script accepts a single argument,
which is the location that the gite data should be 
dumped to.

TODO: add avatars to dump.

Our gitea restore script takes two arguments: the first 
is the zip file from gitea dump, the second is the zip 
file containing user avatars.























