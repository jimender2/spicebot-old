# System Files

In here you will find all the files relating to the bot configuration.
Each section of config is defined by a 'section', denoted with [square brackets].

## Options
### name
This defines the name the bot gives to an IRC "RealName" query.
### nick
This defines the nick the bot uses on IRC.
### user
This is how the bot identifies itself to the IRC server.
### admins
This is where bot administrators are defined by nick.
### host
This defines the server address the bot connects to.
### use_ssl
This tells the bot whether the server uses SSL or not (true or false).
### port
This tells the bot which port to connect on (default for IRC is 6667).
### owner
This defines who the owner of the bot is.
### channels
This is a comma-separated list of the channels the bot will join (including the # symbols beforehand).
### prefix
This defines the 'prefix' the bot uses to identify commands (commands start with this symbol). 
### extra
This defines the full path to where the bot loads modules from. You can add extra folders by separating entries with commas.
### nick_blocks
Any nicks listed here will be ignored by the bot. This is for individual nicks.
### host_blocks
Any hosts/addresses listed here will be blanket ignored by the bot. Any nick signing in from hosts here will be ignored.
### exclude
This lets you exclude files from being loaded at all.
