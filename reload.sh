#!/bin/bash
## Simply reload the bot

## vars
REPODIR=/home/pi/.sopel/github/

## pull modules
git -C $REPODIR pull

## restart service
sudo service sopel restart
