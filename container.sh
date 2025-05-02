#!/bin/bash

# start python container as the current user and group
# with home and current directory mounted

pushd $(dirname "$0") > /dev/null

user=$(id -u -n)
group=$(id -g)

# osx hack, /etc/passwd file does not include the user
cp /etc/passwd ./passwd
echo "$user:*:$(id -u):$(id -g):$user:/home/$user:/bin/bash" >> ./passwd

podman run --rm -ti -v "$PWD:$PWD" -w "$PWD" -v ~:/home/$user/.ssh:ro -v "./passwd:/etc/passwd:ro" -v "/etc/group:/etc/group:ro" -u "$user:$group" python:3.9 bash
