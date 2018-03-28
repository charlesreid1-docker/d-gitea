# d-gitea

Docker files for running gitea

[gitea with docker - documentation](https://docs.gitea.io/en-us/install-with-docker/)

## using the compose file

to get this thing up and running:

```
$ docker-compose up
```

Now visit `<server-ip>:3000`. You will be presented with a configuration page.
Any configuration of gitea will deposit files into `data/`.

Specifically, configuration file will be in `/data/gitea/conf/app.ini`.

On the host machine, you can access named data volumes at 
`/var/lib/docker/volumes/gitea_gitea/_data`
or using `docker cp`.

