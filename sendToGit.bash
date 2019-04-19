#!/bin/bash

if [[ -z "$1" ]] ; then
	exit
fi

git config credential.helper store
git config --global user.name "Clay Brooks"
git config --global user.email "clay_brooks@outlook.com"

mkdir -p results
prior=$PWD
curDir=$(dirname "$0")
resultsFolder=$curDir/results

# go to target directory
cd $1
zip -r -FS $resultsFolder/$USER.zip *
cd $prior

git add $resultsFolder/$USER.zip
git commit -m "Adding results from ${USER}"
git push

