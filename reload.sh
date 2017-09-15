#!/bin/bash
## Simply reload the bot

## vars
GITREPOSITORYURL=
REPODIR=$(dirname $0)
COMPLETEFOLDERPATH=$(realpath $REPODIR)

## stop
sudo service sopel stop

## pull modules
git -C $COMPLETEFOLDERPATH pull

## restart service
sudo service sopel restart
