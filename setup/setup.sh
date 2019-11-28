#!/bin/bash

cd $(dirname $0)

# create the users
cat users | awk -F: '{ printf("adduser --uid %s --disabled-password --gecos \"\" %s\n", $3, $1) }' | sh

# copy in ssh authorized keys
cp -Rp home/* /home

# fix permissions
for user in $(ls /home); do
    chown -R $user:$user /home/$user
done

