# sopel-modules

These are custom modules for sopel

## Commands

[List Of Commands](https://gist.githubusercontent.com/anonymous/564631a78ab7b452530548ec7fe6eedb/raw/3edaf78933f0985a4ef56ec16624f83a0fbab6b8/commands.txt)
______________________________________


(instructions below are for linux)

## Install
`sudo pip install sopel`

#### Then download desired modules to
`~/.sopel/modules/`

`~/.local/lib/python2.7/site-packages/sopel/modules`

`/usr/local/lib/python2.7/dist-packages/sopel/modules`

## service install
`cd /lib/systemd/system/`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/otherfiles/sopel.service`

`sudo systemctl enable sopel.service`

`sudo service sopel start`

`sudo service sopel status`

## dependencies (need to adjust this later)
