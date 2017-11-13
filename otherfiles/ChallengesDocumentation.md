# Duels

Terminology for this documentation:

* Instigator (person who initiated the duel command)

* Target (target of the duel command)

** If not a target, the target equals instigator

Additionally most of the commands can be run with a target such as `.duel stats target-nick`

## Timeouts

* Note: Spicebot has it's own timeout system that should not be confused with Duels!!! You can circumvent some of spicebots timeouts by running the simpler commands in privmsg.

* Upon the conclusion of a duel, a timestamp is set for Channel, Instigator, and Target

* The Channel has a 40 second timeout between duels

* Instigator and target must wait 3 minutes between duels

## Opt In/Out

By default, all users are opted out of duels. To activate duels use `.duel on`

* once you opt In or Out, you may not change your opt status for 1 hour.

* Bot admins can change your status at anytime

## Docs

To reach this documentation simply run `.duel docs`

## Stats

To view all of your current stats run `.duel stats`

## Backpack

To see how many backpack items you have by running `.duel backpack`

## Status

You can view your current enable disable status by running `.duel status`

## Weaponslocker

You can add/del weapons to your personal weaponslocker by using `.duel weaponslocker add barbed-wire`

You may also view some of your locker by running `.duel weaponslocker inv` in privmsg

## Leaderboard

Curious who has the best win/loss ratio,,, run `.duel leader`

## Magic Attack

You must have 250 mana to use this garaunteed win attack. Damage is randomized. `.duel magicattack target`

## Potions

There are three types of potions:

* healthpotion: worth 100 health. Use `.duel healthpotion` to consume.

* poisonpotion: worth -50 health. Use `.duel poisonpotion` to consume.

* manapotion: worth 100 mana. Use `.duel manapotion` to consume.

