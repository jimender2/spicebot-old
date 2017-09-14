# sopel-modules

These are custom modules for sopel

(instructions are for linux)

## Install
`sudo pip install sopel`

#### Then download desired modules to
`~/.sopel/modules/`

## service install
`cd /lib/systemd/system/`

`sudo wget https://raw.githubusercontent.com/deathbybandaid/sopel-modules/master/service/sopel.service`

`sudo systemctl enable sopel.service`

`sudo service sopel start`

`sudo service sopel status`

## dependencies (need to adjust this later)
`sudo pip install IPython`

`sudo pip install fake_useragent`
