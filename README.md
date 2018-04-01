# d-gitea

Docker files for running gitea

[gitea with docker - documentation](https://docs.gitea.io/en-us/install-with-docker/)

## custom gitea files

the main use of this container is part of the larger charlesreid1 pod,
so the main purpose of this repo is to store custom gitea files.

These are stored in `custom/`.

`custom/` should map to `/data/gitea/` inside the container.

## using the compose file

to get this thing up and running:

```
$ docker-compose up
```

Now visit `<server-ip>:3000`. You will be presented with a configuration page.
Set up the gitea instance. This will automatically populate the directory 
structure. See below for more info.

## directory structure

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
│   └── repositories
│       └─e charlesreid1
│           └── oieruoweiur.git
│               ├── branches
│               ├── config
│               ├── description
│               ├── HEAD
│               ├── hooks
│               │   ├── applypatch-msg.sample
│               │   ├── commit-msg.sample
│               │   ├── post-receive
│               │   ├── post-receive.d
│               │   │   └── gitea
│               │   ├── post-update.sample
│               │   ├── pre-applypatch.sample
│               │   ├── pre-commit.sample
│               │   ├── prepare-commit-msg.sample
│               │   ├── pre-push.sample
│               │   ├── pre-rebase.sample
│               │   ├── pre-receive
│               │   ├── pre-receive.d
│               │   │   └── gitea
│               │   ├── pre-receive.sample
│               │   ├── update
│               │   ├── update.d
│               │   │   └── gitea
│               │   └── update.sample
│               ├── info
│               │   ├── exclude
│               │   └── refs
│               ├── objects
│               │   ├── info
│               │   │   └── packs
│               │   └── pack
│               └── refs
│                   ├── heads
│                   └── tags
├── gitea
│   ├── conf
│   │   └── app.ini
│   ├── gitea.db
│   ├── indexers
│   │   └── issues.bleve
│   │       ├── index_meta.json
│   │       └── store
│   ├── lfs
│   ├── log
│   │   ├── gitea.log
│   │   ├── http.log
│   │   └── xorm.log
│   └── sessions
│       └── oauth2
└── ssh [error opening dir]

25 directories, 29 files
```

## backup and restore

Fortunately, gitea provides dump functionality.

Unfortunately, there is no restore functionality.

The dump functionality creates a zip with
the following struture:

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



