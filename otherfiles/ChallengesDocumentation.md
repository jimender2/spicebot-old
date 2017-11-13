# Duels

Terminology for this documentation:

* Instigator (person who initiated the duel command)

* Target (target of the duel command)

** If not a target, the target equals instigator

Additionally most of the commands can be run with a target such as `.duel stats target-nick`

Commands that target other users, detect if the other user is in the room, and if they have duels enabled.

## Duel

* Duels cannot be initiated in privmsg, but the other commands can

* You cannot duel yourself, or the bot

* You cannot duel those that are not in the room, on a timeout, or have duels disabled.

* You may not duel the same person twice in a row.

* You can attack a random person using `.duel random`

* weapon is selected from personal weaponslocker unless manually specified `.duel target awesome-weapon`

### Actual combat process

* Check that Instigator and Target have health, if not give them 1000 health

* Instigator has a random chance of finding a loot item, but if they lose the current duel, the winner takes the loot.

* Winner is selected by a complex dice roll setup (d20)

** Each Player gets 1 roll

** Instigator gets an extra roll for initiating the attack

** The person with more XP points gets an extra roll

** Coinflip gives lucky person an extra roll

** the results of the dice rolls are stored in an array, and the largest number is the one used

** player with the highest number wins

* weapon is selected from personal weaponslocker unless manually specified

* Damage is randomized.

* winner gains 5 XP, loser gains 3 XP

* If the winner kills the oponent, all backpack items in losers inventory now belong to the winner.

## Health Regeneration

An incentive for Being in the channel:

Every 30 minutes, if your health is below 500, you will gain 50 health.

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

* healthpotion: worth 100 health. Use `.duel healthpotion` to consume.

* poisonpotion: worth -50 health. Use `.duel poisonpotion` to consume.

* manapotion: worth 100 mana. Use `.duel manapotion` to consume.

* mysterypotion: With unknown effects! Use `.duel mysterypotion` to consume.

* timepotion: worth 180 seconds of timeout. Use `.challenge timepotion` to consume 

Potions can either be used on yourself, or on others.
