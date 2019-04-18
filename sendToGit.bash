#!/bin/bash

if [[ -z "$1" ]] ; then
	exit
fi

git config credential.helper store
git config --global user.name "Clay Brooks"
git config --global user.email "clay_brooks@outlook.com"

zip -r results/$USER.zip $1

git add $USER.zip
git commit -m "Adding results from ${USER}"
git push

