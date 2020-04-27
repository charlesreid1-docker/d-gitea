#!/bin/bash
set -x

# secret_key and internal_token should be SIMPLE or this 
# gets screwy, and I don't want to do any more debugging.
# 
cat custom/conf/app.ini.sample \
  | sed 's/REPLACEME_INTERNALTOKEN_SECRET/'$(cat internal_token.secret)'/g' \
  | sed 's/REPLACEME_SECRETKEY_SECRET/'$(cat secret_key.secret)'/g'  > custom/conf/app.ini
