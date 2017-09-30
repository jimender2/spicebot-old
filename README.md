# SpiceBot

These are custom modules for Spicebot

## Commands

[List Of Commands](https://github.com/deathbybandaid/sopel-modules/blob/master/otherfiles/commands.MD)
______________________________________


(instructions below are for raspberry pi)

## Install
`sudo pip install sopel`

#### Then download desired modules to
`~/.sopel/modules/`

##### Github Linkage for modules

`cd ~/.sopel/`

`sudo git clone https://github.com/deathbybandaid/sopel-modules.git spicebot`

`sudo chown -R pi:pi spicebot`

`sudo git clone https://github.com/deathbybandaid/sopel-modules.git spicebotdev`

`sudo chown -R pi:pi spicebotdev`

`cd spicebotdev`

`sudo git checkout dev`

##### Default Module Locations
`~/.local/lib/python2.7/site-packages/sopel/modules`

`/usr/local/lib/python2.7/dist-packages/sopel/modules`

### configs

`cd ~/.sopel/`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/configs/spicebot.cfg`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/dev/configs/spicebotdev.cfg`

## service install
`cd /lib/systemd/system/`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/gonfigs/spicebot.service`

`sudo systemctl enable spicebot.service`

`sudo service sopel spicebot`

`sudo service sopel spicebot`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/configs/spicebotdev.service`

`sudo systemctl enable spicebotdev.service`

`sudo service sopel spicebotdev`

`sudo service sopel spicebotdev`

## dependencies (need to adjust this later)

### arrow

`sudo git clone https://github.com/crsmithdev/arrow.git`

`cd arrow`

`sudo pip install -r requirements.txt`

`sudo pip install -e`
