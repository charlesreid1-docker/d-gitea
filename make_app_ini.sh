#!/bin/bash
set -x

# secret_key and internal_token
# should be SIMPLE or this 
# gets screwy. 
# 
# I'm too sick and tired of stupid scripting problems to fix this.
# Like, OF COURSE IT DOESN'T WORK
# 
cat app.ini.sample \
  | sed 's/REPLACEME_INTERNALTOKEN_SECRET/'$(cat internal_token.secret)'/g' \
  | sed 's/REPLACEME_SECRETKEY_SECRET/'$(cat secret_key.secret)'/g'  > app.ini
