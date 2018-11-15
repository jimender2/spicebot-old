#!/bin/sh
##RUN ALL AS ROOT
#install package for streaming audio out
apt-get install icecast2
## note down passwords set during install
## set ENABLE=true in /etc/default/icecast2 once config done

#install packages for test audio playback
apt-get install mpd mpc
## enable shout output from /etc/mpd.conf
## configure "mount" as /mpd and place some test audio in /var/lib/mpd/music
## set password to match icecast stream password
## run the following: 
## "mpc clear && mpc update"
## "ls /var/lib/mpd/music | mpc add"
## "mpc listall && mpc random on && mpc repeat on && mpc play"
## if mpc refuses connection, kill all instances of mpd via htop
## Use whatever folder you like for the music files.