# sopel-modules

These are custom modules for sopel

## Commands

8BALL           8ball

ADMIN           save  quit  msg  part  me  join  set  mode

ADMINCHANNEL    unquiet  topic  kickban  kick  tmask  showmask  quiet
                unban  ban

ANNOUNCE        announce

ASIMOV          asimov

CALC            py  c

CLAIMNEWUSER    pee

CLOCK           settz  settimeformat  getchanneltz  t  gettz
                setchanneltimeformat  gettimeformat  setchanneltz
                getchanneltimeformat

CORETASKS       blocks  useserviceauth

COUNTDOWN       countdown

CURRENCY        btc  cur

DEVEXCUSE       devexcuse

DICE            choose  d

DUEL            duelon  dueloff  duels  duelself  duel

ETYMOLOGY       ety

FERENGI         ferengi

FUCKINGWEATHER  fucking_weather

HELP            help

IP              iplookup

IPYTHON         console

ISUP            isup

LMGTFY          lmgtfy

MEETBOT         agreed  info  comment  action  subject  listactions
                link  chairs  comments  endmeeting  startmeeting

MERAKI          meraki

MOVIE           movie

PACKT           packt

POINTS          points

RAND            rand

REDDIT          redditor  setsafeforwork  getsafeforwork

RELOAD          update  load  reload

REMIND          in  at

RICKROLL        rickroll

ROULETTE        roulette-stop  roulette

RULES           rules1  rules3  rules2  rules5  rules4  rules7  rules6
                rules9  rules8  rules  rules14  rules11  rules10
                rules13  rules12

SAFETY          safety

SEARCH          duck  suggest  search

SEEN            seen

SPELLCHECK      spellcheck

SPICEBOTRELOAD  spicebotreload

SPICECONTESTS   swcontests

SPICEMODULES    spicemodules

SYSADMINTOOLS   sysadmintools

TECHSUPPORT     techsupport

TELL            tell

TLD             tld

TRANSLATE       translate  mangle

UNICODE_INFO    u

UNITS           temp  length  weight

UPTIME          uptime

URBAN           urban

URL             title

VERSION         version

WEATHER         setlocation  weather

WIKIPEDIA       w

WIKTIONARY      wt

XKCD            xkcd

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
