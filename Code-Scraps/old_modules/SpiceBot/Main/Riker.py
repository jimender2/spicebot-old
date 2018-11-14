#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2


@sopel.module.commands('riker')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, trigger.group(1))
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    data = "For an android with no feelings, he sure managed to evoke them in others. We have a saboteur aboard. I will obey your orders. I will serve this ship as First Officer. And in an attack against the Enterprise, I will die with this crew. But I will not break my oath of loyalty to Starfleet. Not if I weaken first. Worf, It\'s better than music. It\'s jazz. I think you\'ve let your personal feelings cloud your judgement. That might\'ve been one of the shortest assignments in the history of Starfleet. Some days you get the bear, and some days the bear gets you. Maybe if we felt any human loss as keenly as we feel one of those close to us, human history would be far less bloody. Talk about going nowhere fast. In all trust, there is the possibility for betrayal. A surprise party? Mr. Worf, I hate surprise parties. I would *never* do that to you. Is it my imagination, or have tempers become a little frayed on the ship lately? Fate protects fools, little children and ships named Enterprise. What\'s a knock-out like you doing in a computer-generated gin joint like this? But the probability of making a six is no greater than that of rolling a seven. How long can two people talk about nothing? Besides, you look good in a dress. Why don\'t we just give everybody a promotion and call it a night - \'Commander\'? The look in your eyes, I recognize it. You used to have it for me. You enjoyed that. The game\'s not big enough unless it scares you a little. Well, I\'ll say this for him - he\'s sure of himself. This should be interesting. Yesterday I did not know how to eat gagh. They were just sucked into space. Wouldn\'t that bring about chaos? Shields up! Rrrrred alert! My oath is between Captain Kargan and myself. Your only concern is with how you obey my orders. Or do you prefer the rank of prisoner to that of lieutenant? I suggest you drop it, Mr. Data. About four years. I got tired of hearing how young I looked. Your shields were failing, sir. You bet I\'m agitated! I may be surrounded by insanity, but I am not insane. Sorry, Data. Sure. You\'d be surprised how far a hug goes with Geordi, or Worf. The unexpected is our normal routine. The Enterprise computer system is controlled by three primary main processor cores, cross-linked with a redundant melacortz ramistat, fourteen kiloquad interface modules. Did you come here for something in particular or just general Riker-bashing? Computer, lights up! Wait a minute - you\'ve been declared dead. You can\'t give orders around here. Commander William Riker of the Starship Enterprise. Mr. Worf, you do remember how to fire phasers? Fear is the true enemy, the only enemy. Yes, absolutely, I do indeed concur, wholeheartedly! I\'m afraid I still don\'t understand, sir. I\'ll be sure to note that in my log. I can\'t. As much as I care about you, my first duty is to the ship. Captain, why are we out here chasing comets? Now we know what they mean by \'advanced\' tactical training. Travel time to the nearest starbase? Earl Grey tea, watercress sandwiches... and Bularian canapes? Are you up for promotion? You did exactly what you had to do. You considered all your options, you tried every alternative and then you made the hard choice. This is not about revenge. This is about justice. Computer, belay that order. When has justice ever been as simple as a rule book? I\'d like to think that I haven\'t changed those things, sir. Now, how the hell do we defeat an enemy that knows us better than we know ourselves? I\'ll alert the crew. Maybe if we felt any human loss as keenly as we feel one of those close to us, human history would be far less bloody. Mr. Crusher, ready a collision course with the Borg ship. Ensign Babyface! Smooth as an android\'s bottom, eh, Data? Mr. Worf, you sound like a man who\'s asking his friend if he can start dating his sister. I am your worst nightmare! Fate. It protects fools, little children, and ships named \"Enterprise.\" We could cause a diplomatic crisis. Take the ship into the Neutral Zone Flair is what marks the difference between artistry and mere competence. Our neural pathways have become accustomed to your sensory input patterns. Could someone survive inside a transporter buffer for 75 years? and attack the Romulans. Then maybe you should consider this: if anything happens to them, Starfleet is going to want a full investigation. I\'ve had twelve years to think about it. And if I had it to do over again, I would have grabbed the phaser and pointed it at you instead of them. And blowing into maximum warp speed, you appeared for an instant to be in two places at once. We know you\'re dealing in stolen ore. But I wanna talk about the assassination attempt on Lieutenant Worf. Maybe we better talk out here; the observation lounge has turned into a swamp. Well, that\'s certainly good to know. I guess it\'s better to be lucky than good. We finished our first sensor sweep of the neutral zone. What? We\'re not at all alike! Your head is not an artifact! Some days you get the bear, and some days the bear gets you. I recommend you don\'t fire until you\'re within 40,000 kilometers. You\'re going to be an interesting companion, Mr. Data. Congratulations - you just destroyed the Enterprise. A lot of things can change in twelve years, Admiral. Damage report! The Federation\'s gone; the Borg is everywhere! When has justice ever been as simple as a rule book?"

    dataa = data.split(" ")
    ma = spicemanip(bot, triggerargsarray, 1)
    message = ""

    if not ma:
        max = 13
    else:
        max = int(ma)
        if max <= 0:
            max = 13
        else:
            max = max - 1

    times = 1
    t = 1

    if max > 963:
        max = 962
        msg = "Sorry. I can only do up to 963 words. Here are 963 words and if you need more you can do Ctrl + C / Ctrl + V"
        osd(bot, trigger.sender, 'say', msg)

    i = 0
    while i <= max:
        message = message + dataa[i] + " "
        i = i + 1

    osd(bot, trigger.sender, 'say', message)
