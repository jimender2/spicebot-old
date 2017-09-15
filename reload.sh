#!/bin/bash
## Simply reload the bot

## vars
REPODIR=$(dirname $0)
COMPLETEFOLDERPATH=$(realpath $REPODIR)

## pull modules
git -C $COMPLETEFOLDERPATH pull

## restart service
sudo service sopel restart
