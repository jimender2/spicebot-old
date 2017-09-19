# sopel-modules

These are custom modules for sopel

## Commands

[List Of Commands](https://gist.github.com/anonymous/15e7b91d2d434a774b9ccce3af186bf6)
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
