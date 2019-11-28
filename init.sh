#!/bin/sh
#
# Gather non-system users and authorized keys to set up in container
#
cat /etc/passwd | awk -F: '{ if ($3 >= 1000 && $3 <= 2000) print $0 }' > setup/users
mkdir -p setup/home && chmod 700 setup/home
for user in $(cat setup/users | cut -d: -f1); do
    mkdir -p setup/home/$user/.ssh && chown -R $user:$user setup/home/$user
    if [ -e /home/$user/.ssh/id_rsa.pub ]; then
        cp -p /home/$user/.ssh/id_rsa.pub setup/home/$user/.ssh/authorized_keys
    fi
done
