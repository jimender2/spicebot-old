#!/bin/bash
## Simply reload the bot

## vars
REPODIR=$(dirname $0)

## pull modules
sudo git -C $REPODIR pull

## restart service
sudo service sopel restart
