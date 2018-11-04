#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
import urllib
from xml.dom.minidom import parseString
import sys
import os
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
from BotShared import *

# author jimender2

replies = [
            "Ash: Yeah! [after shooting King Arthur's sword in half]",
            "Ash: Alright you Primitive Screwheads, listen up! You see this? This... is my BOOMSTICK! The twelve-gauge double-barreled Remington. S-Mart's top of the line. You can find this in the sporting goods department. That's right, this sweet baby was made in Grand Rapids, Michigan. Retails for about a hundred and nine, ninety five. It's got a walnut stock, cobalt blue steel, and a hair trigger. That's right. Shop smart. Shop S-Mart. You got that?",
            "Ash: [voiceover] Sure, I could have stayed in the past. I could have even been king. But in my own way, I *am* king. [Ash grabs girl close]",
            "Ash: Hail to the king, baby. [Ash kisses the girl]",
            "Ash: Good. Bad. I'm the guy with the gun.",
            "[Upon getting the powered glove in place of his right hand] Ash: Groovy.",
            "[In a passionate moment of romance] Ash: Gimme some sugar, baby.",
            "Duke Henry: You Sir, are not one of my vassals... who are you?",
            "Ash: Who wants to know?",
            "Duke Henry: I am Henry the Red. Duke of Shale, Lord of the Northlands and leader of its peoples.",
            "Ash: Well hello Mister Fancypants. Well, I've got news for you pal, you ain't leadin' but two things, right now: Jack and shit... and Jack left town.",
            "Old Woman: I'll swallow your soul!",
            "Ash: Come get some.",
            "Sheila: You found me beautiful once...",
            "Ash: Honey, you got reeeal ugly!",
            "Ash: [to the Witch] Yo, she-bitch! Let's go!",
            "Arthur: Are all men from the future loud-mouthed braggarts?",
            "Ash: Nope. Just me baby... Just me.",
            "Ash: Hail to the king, baby.",
            "Ash: Klaatu Barada N... necktie... nectar... nickel... noodle. It's an \"N\" word, it's definitely an \"N\" word! Klaatu... Barada... N... [coughs]",
            "Ash: [pause] Okay then... that's it!]",
            "Ash: Lady, I'm afraid I'm gonna have to ask you to leave the store.",
            "Possessed woman: Who the hell are you?",
            "Ash: Name's Ash. [cocks rifle]",
            "Ash: Housewares.",
            "Ash: What are you? Are you me?",
            "Evil Ash: Whad are do? Are do be? HAHAHAHAHAH! You sound like a jerk!",
            "Ash: Why ya doin' this, huh?",
            "Evil Ash: Oh, you wanna know? 'Cause the answer's easy! I'm BAD Ash... and you're GOOD Ash! You're a goody little two-shoes! Little goody two-shoes! Little goody two-shoes! [begins to sucker-punch Ash]",
            "Evil Ash: Goody little TWO-SHOES! Goody little TWO-SHOES! HEHEHEHEHE! [honk honk honk]",
            "Evil Ash: GOODY LITTLE TWO-SHOES! GOODY LITTLE...",
            "Ash: [cocks shotgun and points it under Evil Ash's nose][nods head and shoots him]",
            "Ash: Good. Bad. I'm the guy with the gun.",
            "Ash: Klaatu Barada Nikto.",
            "Wiseman: Well, repeat them.",
            "Ash: Klaatu Barada Nikto.",
            "Wiseman: Again.",
            "Ash: I got it, I got it! I know your damn words, alright?",
            "Sheila: I may be bad... but I feel gooood.",
            "Ash: Don't touch that please, your primitive intellect wouldn't understand alloys and compositions and things with... molecular structures.",
            "Evil Ash: You'll never retrieve the Necronomicon! You'll die before ya get it!",
            "Ash: Hey! What's that you got on your face? Evil Ash: Huh? [Ash throws dirt on Evil Ash's face]",
            "Ash: See how that works?",
            "Wiseman: When you removed the book from the cradle, did you speak the words?",
            "Ash: Yeah, basically.",
            "Wiseman: Did you speak the exact words?",
            "Ash: Look, maybe I didn't say every single little tiny syllable, no. But basically I said them, yeah.",
            "Ash: It's a trick. Get an axe.",
            "Ash: My name is Ash and I am a slave. Close as I can figure, the year is thirteen hundred A.D and I'm being dragged to my death. It wasn't always like this, I had a real life, once. A job.",
            "Ash: [now Ash is in a flashback] Umm... Hardware aisle twelve, shop smart, shop S-Mart!",
            "Ash: [back to monologue] I had a wonderful girlfriend Linda. Together we drove to a small cabin in the mountains. It seems an archeologist had come to this remote place to translate and study his latest find: Necronomiconexmortis. The Book of the Dead. Bound in human flesh and inked in blood, this ancient Samarian text contained bizarre burial rights, funeral incantations, and demon resurrection passages, it was never meant for the world of the living. The book awoke something dark in the woods, something evil. [something crashes through the window of the cabin and Linda screams]",
            "Ash: It took Linda. Then it came after me, it got into my hand and it went bad, so I lopped it off at the wrist. [Ash is seen cutting off his hand]",
            "Ash: But that didn't stop it, it came back big time.",
            "Ash: [Ash gets pulled into the vortex holding onto the doorway] For God's sake how do you stop it?",
            "Sheila: But what of all those sweet words you spoke in private?",
            "Ash: Oh that's just what we call pillow talk, baby, that's all.",
            "Evil Ash: I got a bone to pick with you.",
            "Ash: Maybe. Just maybe my boys can protect the book. Yeah, and maybe I'm a Chinese jet pilot.",
            "[Sheila wants to apologize to Ash] Ash: First you wanna kill me, now you wanna kiss me. Blow.",
            "Ash: [trying to kill a small Ash that has jumped into his mouth and into his stomach, he gets a kettle of boiling water] Okay, little fella, here's a little hot chocolate for ya! Ha ha ha ha ha ha!",
            "Evil Ash: You're pissing me off, you ugly son of a bitch!",
            "Ash: Alright. Who wants some? [as undead Ash stands triumphant on catapult]",
            "Ash: Buckle up Bonehead. 'Cause you're goin' for a ride!",
            "[as an evil Ash begins growing out of his shoulder] Ash: Oh, dear God, it's growing bigger!",
            "[when Sheila walks into the blacksmith's shop to talk to Ash] Ash: What? Were you raised in a barn? Shut the door! Probably was raised in a barn, along with the other primitives.",
            "Ash: Keep your damn filthy bones outta my mouth.",
            "Skeleton: Let's get the hell out of here!",
            "Evil Ash: You're going down!",
            "Ash: I'm going up!",
            "Ash: Oh you little bastards! All right, I'll crush each and every last one of ya! I'll squash you so hard you'll have to look down to look up!",
            "Mini Ash: Hey dumbass!",
            "Ash: Now I swear the next one of you primates even *touches* me...",
            "Ash: Now whoa whoa whoa right there spinach chin!",
            "Ash: That's it, go ahead and run. Run home and cry to mama!",
            "[to his skeleton minions, who are digging up corpses in a graveyard] Evil Ash: Dig, damn you! Dig faster! I shall command every worm-infested son-of-a-bitch that ever died in battle!",
            "Skeleton: Thank you, sir!",
            "Ash: We can take these Deadites, we can take 'em! With science.",
            "Sheila: [after been converted by the deadites, she pulls back her veil revealing a rather pasty looking complexion] I may be bad, but I feel... good.",
            "Evil Ash: Oh, you miserable bags of bones! Pick yourselves up and sally fo-, sally for-, sally forth.",
            "Ash: [as a soldier blocks his way, he pushes him aside] Get the fuck out of my face!",
            "Arthur: How will we stop an army of the dead at our castle walls? How will you fight that? With more words? Most of our people have already fled. We are but sixty men.",
            "Evil Ash: [Admiring Sheila] Well aren't you the sweetest little thing?",
            "Sheila: [Being handled by Evil Ash] Don't touch me! You foul thing!",
            "Evil Ash: You're gonna learn to love me, missy.",
            "Sheila: The Promised one will come for you.",
            "Evil Ash: Darlin' I'm gonna save him the trouble.",
            "Old Woman: Into the pit with those bloody-thirsty sons of whores!",
            "Soldier: [stabbing at Ash's car] What a piece of armor this is!",
            "Ash: Say hello to the twenty-first century!",
            "[Ash emerges from a cave where he's been asleep for 700 years. He looks overjoyed] Ash: Ha ha. Manufactured parts. Ha...",
            "[Look of joy turns to horror as he sees a world devastated by nuclear war] Ash: No. No. Oh God I slept too long!",
            "Ash: [as the credits start] Hahahahahahahahaha...",
            "Ash: [after being sucked into a blackhole in a fake copy of the Necronomicon and struggling back out] Whoa. Wrong book.",
            "Ash: [to Arthur] You know your shoe lace is untied.",
            "Ash: I know you're scared; we're all scared, but that doesn't mean wee cowards. We can take these skeletons, we can take them, with science.",
            "Skeleton: [Upon seeing demonic Sheila] There's a sight for sore bones.",
            "Ash: [after reaching the location of the Necronomicon, and finding three identical books]",
            "[scratches himself in the head] Ash: Three books? Wait a minute... Hold it... Nobody said anything about three books!",
            "Ash: London bridge is falling down, falling down, falling doown!",
            "[steps on a nail held by the mini Ashes] Mini Ashs: My fair lady ha!",
            "Skeleton: [dragging topless wench] We got plans for you, Girlie-girl!",
            "Skeleton: I'll cut off your gizzard.",
            "Deadite Captain: [pulling a newly animated skeleton from the grave] Welcome back to the land of the livin'... NOW PICK UP A SHOVEL AND GET DIGGING!",
            "Deadite Captain: Cry Havoc and let loose the Dogs of War!",
            "Ash: [to himself] Like, like what am I supposed to do - take one book, or all books, or what?",
            "Ash: So what's the deal? Can you send me back or not?",
            "Wiseman: Only the Necronomicon has the power. An unholy book which we also require. Within its pages are passages that can send you back to your time. Only you the promised one can quest for it.",
            "Ash: I don't want your book, I don't want your bullshit. Just send me back to my own time, pronto, today. Chop chop!",
            "Cowardly Warrior: You can count on my steel.",
            "Ash: [after crushing skeletons with boulders] Ooh that's gotta hurt.",
            "Evil Ash: I'll spoil those good looks back stabber.",
            "Skeleton: [during the battle, and the undead start ramming the castle gate] Jeez, put your backbones into it!"]


@sopel.module.commands('ash')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'ash')
    if not enablestatus:
        # IF "&&" is in the full input, it is treated as multiple commands, and is split
        commands_array = spicemanip(bot, triggerargsarray, "split_&&")
        if commands_array == []:
            commands_array = [[]]
        for command_split_partial in commands_array:
            triggerargsarray_part = spicemanip(bot, command_split_partial, 'create')
            execute_main(bot, trigger, triggerargsarray_part, botcom, instigator)


def execute_main(bot, trigger, triggerargsarray, botcom, instigator):
    answer = spicemanip(bot, replies, 'random')
    osd(bot, trigger.sender, 'say', answer)
