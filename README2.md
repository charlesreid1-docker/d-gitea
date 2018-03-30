# Next Round of Additions

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
