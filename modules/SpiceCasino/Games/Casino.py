#!/usr/bin/env python
# coding=utf-8
from __future__ import unicode_literals, absolute_import, print_function, division
import sopel.module
from sopel import module, tools
import sys
import os
import random
moduledir = os.path.dirname(__file__)
shareddir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(shareddir)
sys.path.append(moduledir)
from BotShared import *
import Spicebucks

#shared variables:
maxbet = 100
now = time.time()
slottimeout = 5
#rouletteshared
roulettetimeout=25
#maxwheel = get_database_value(bot,'casino','maxwheel')

#Lotteryshared
match1payout = 2
match2payout = 4
match3payout = 0.1#% of jackpot
match4payout = 0.3 #% of jackpot
#lotterytimeout=1790
#lotterymax = get_database_value(bot,'casino','lotterymax')

wikiurl = 'https://github.com/deathbybandaid/SpiceBot/wiki/Casino'

@sopel.module.commands('gamble', 'casino')
def mainfunction(bot, trigger):
    enablestatus, triggerargsarray, botcom, instigator = spicebot_prerun(bot, trigger, 'gamble')
    if not enablestatus:
        execute_main(bot, trigger, triggerargsarray, botcom, instigator)

def execute_main(bot, trigger, arg, botcom, instigator):
    mygame = get_trigger_arg(bot, arg, 1) or 'nocommand'
    if mygame == 'docs' or mygame == 'help':
        bot.say("For help with this module, see here: " + wikiurl)
    elif mygame =='slots':
        slots(bot,trigger,arg)
    elif mygame=='blackjack':
        blackjack(bot,trigger,arg)
    elif (mygame=='roulette' or mygame=='spin'):
        roulette(bot,trigger,arg)
    elif mygame=='lottery':
        lottery(bot,trigger,arg)
    elif mygame== 'freebie':
        freebie(bot,trigger)
    elif mygame == 'bank':
        bankbalance=Spicebucks.bank(bot,trigger.nick)
        bot.notice(trigger.nick + ' has ' + str(bankbalance) + ' spicebucks in the bank.', trigger.nick)
    elif mygame == 'jackpot':
        bankbalance=Spicebucks.bank(bot,'SpiceBank')
        bot.say('The current jackpot is: ' +str(bankbalance))
    elif mygame=='admin':
        if trigger.admin or trigger.nick == 'under_score':
            admincommands(bot,trigger,arg)
        else:
             bot.notice('You must be an admin to use this command', trigger.nick)
    else:
        bot.say('Please choose a game. Options include: slots, blackjack, roulette, and lottery.')

def freebie(bot,trigger):
    bankbalance=Spicebucks.bank(bot,trigger.nick) or 0
    spicebankbalance=Spicebucks.bank(bot, 'SpiceBank') or 0
    if bankbalance<1:
        if spicebankbalance >=1:
            bot.notice('The casino gives you 1 Spicebuck for use in the casino', trigger.nick)
            Spicebucks.transfer(bot, 'SpiceBank', trigger.nick, 1)
        else:
            bot.notice("The casino doesn't have any funds to provide",trigger.nick)
    else:
        bot.notice(('Looks like you dont need a handout because your bank balance is ' + str(bankbalance)),trigger.nick)

def slots(bot,trigger,arg):
#_____________Game 1 slots___________
#slot machine that uses computer terms with a jackpot tied to how much money has been gambled
    player=trigger.nick
    channel=trigger.sender
    now = time.time()
#__payouts___
    match3 = 25
    match2 = 5
    bankbalance=Spicebucks.bank(bot,'SpiceBank')
    if bankbalance <=500:
        bankbalance=500
        set_database_value(bot,'SpiceBank', 'spicebucks_bank',  bankbalance)

    keyword = get_database_value(bot, 'casino','slotkeyword') or 'BSOD'
    #match3jackpot = jackpot or 500
    mychoice = get_trigger_arg(bot, arg, 2) or 'nocommand'
    if mychoice == 'payout':
            bot.say("Today's jackpot word is " + keyword + " getting it three times will get you " + str(bankbalance) + ". Match 3 and get " + str(match3))
    else:
#start slots
        if not channel.startswith("#"):
            bot.notice(trigger.nick + ", slots can only be used in a channel.", player)
        else:
            lastslot = get_database_value(bot,'casino','slotimer')
            nextslot = get_timesince(bot,'casino','slotimer')

            if nextslot>=slottimeout:
                if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', 1) == 1:
                    set_database_value(bot,'casino','slotimer',now)
                    #add bet to spicebank
                    mywinnings = 0

                    wheel = get_database_value(bot, 'casino','slotwheel') or []
                    if wheel ==[]:
                        wheel = ['BSOD', 'RAM', 'CPU', 'RAID', 'VLANS', 'WIFI', 'ClOUD']
                    wheel1 = spin(wheel)
                    wheel2 = spin(wheel)
                    wheel3 = spin(wheel)
                    reel = [wheel1, wheel2, wheel3]
                    bot.say(trigger.nick + ' inserts 1 spicebuck and the slot machine displays | ' + wheel1 + ' | ' + wheel2 + ' | ' + wheel3 + ' | ')
                    for i in reel:
                        if i==keyword:
                            mywinnings = mywinnings + 1
                    if mywinnings>=1:
                        bot.notice(('You got a bonus word, ' + keyword + ', worth 1 spicebuck'), player)

                    if(wheel1 == wheel2 and wheel2 == wheel3):
                        if wheel1 == keyword:
                            bot.say(trigger.nick + ' hit the Jackpot of ' + str(bankbalance))
                            mywinnings=bankbalance
                        elif wheel1 == 'Patches':
                            mywinnings= mywinnings + match3
                        else:
                            mywinnings= mywinnings + match3
                    elif(wheel1 == wheel2 or wheel2==wheel3 or wheel3==wheel1):
                        mywinnings =  mywinnings + match2
                        #bot.say(trigger.nick + ' a match')

                    if mywinnings <=0:
                        bot.say(trigger.nick + ' gets nothing')
                    else:
                        bankbalance=Spicebucks.bank(bot,'SpiceBank')
                        if mywinnings > bankbalance:
                            Spicebucks.spicebucks(bot, trigger.nick, 'plus', mywinnings)
                            bot.say(trigger.nick + ' wins ' + str(mywinnings))
                        else:
                            if Spicebucks.transfer(bot, 'SpiceBank', trigger.nick, mywinnings) == 1:
                                bot.say(trigger.nick + ' wins ' + str(mywinnings) + " spicebucks")
                            else:
                                bot.say('Error in banking system')
                else:
                    bot.notice("You don't have enough Spicebucks",player )
            else:
                bot.notice("You can not use the slot machine for " + str(hours_minutes_seconds((slottimeout-nextslot))),player)

#------Start Roulette
#----------------Roulette-------
def roulette(bot,trigger,arg):
    now = time.time()
    channel = trigger.sender
    maxwheel = int(get_database_value(bot,'casino','maxwheel')) or 24

    minbet=15 #requires at least one payday to play
    wheel = range(maxwheel + 1)
    colors = ['red', 'black']
    inputcheck = 0
    maxplayers = 3
    callcheck = False
    player = trigger.nick

    mybet = get_trigger_arg(bot, arg, 2) or 'nobet'
    myitem = get_trigger_arg(bot, arg, 3) or 'noitem'
    myitem2 = get_trigger_arg(bot, arg, 4) or 'noitem'

#__payouts___
    colorpayout = 2 #% of amount bet + amount bet
    #numberpayout = amount bet * numbers of maxwheel

    if not channel.startswith("#"):
        bot.notice(trigger.nick + ", roulette can only be used in a channel.", player)
    else:
        #set bet/check for commands
        if mybet == 'nobet':
            bot.say('Please enter an amount to bet')
            inputcheck = 0
        elif mybet=='payout':
            bot.say('Picking the winng number will get you ' + str(maxwheel) + ' X your bet. Picking the winning color will get you your bet plus half the amount bet')
        elif mybet =='call':
            players = get_database_value(bot, 'casino', 'rouletteplayers') or []
            for i in players:
                if i == player:
                    bot.say(trigger.nick + " has asked Spicebot to finish the roulette game. Last call for bets")
                    set_database_value(bot,'casino','casinochannel',str(trigger.sender))
                    set_database_value(bot,'casino','counter','roulette')
                    set_database_value(bot,'casino','countertimer',now)
                    callcheck = True
            if not callcheck:
                bot.notice("You must first place a bet",player)

        else:
            if mybet == 'allin':
                balance = Spicebucks.bank(bot, trigger.nick)
                if balance > 0:
                    mybet=balance
                    if myitem.isdigit():
                        myitem2 = 'noitem'
                        inputcheck = 1
                    else:
                        bot.notice("You can only bet on a number going all in.",player)
                else:
                    bot.notice('You do not have any spicebucks',player)
                    inputcheck = 0
            elif not mybet.isdigit():
                bot.notice(('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet)),player)
                inputcheck = 0
            else:
                inputcheck = 1
                mybet = int(mybet)
                if (mybet<minbet or mybet>maxbet):
                    bot.notice(('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet)), player)
                    inputcheck = 0
        #setup what was bet on
            if inputcheck == 1:
                #check to see if a number was entered
                mynumber=''
                mycolor = ''
                if myitem.isdigit():
                    mynumber = int(myitem)
                    if(mynumber < 1 or mynumber > maxwheel):
                        bot.notice(('Please pick a number between 1 and ' + str(maxwheel)),player)
                        inputcheck=0
                        #check to see if a color was selected
                    else:
                        if not myitem2 == 'noitem':
                            if (str(myitem2) == 'red' or str(myitem2) == 'black'):
                                mycolor = myitem2
                            else:
                                bot.notice(('Choose either red or black'), player)
                                inputcheck=0
                                mycolor=''
                        else:
                            mycolor = ''
                            inputcheck =1
            #was a color selected first
                elif(myitem == 'red' or myitem == 'black'):
                    mycolor = myitem
                    mynumber=''
                    inputcheck =1
                else:
                    #no valid choices
                    bot.notice(('Please pick either a color or number to bet on'),player)
                    inputcheck = 0

        # user input now setup game will run
        if inputcheck == 1:
            players = get_database_value(bot, 'casino', 'rouletteplayers') or []
            for i in players:
                if i == player:
                    bot.notice("You already placed a bet",player)
                    inputcheck = 0
            if inputcheck == 1:
                if Spicebucks.transfer(bot, trigger.nick, 'SpiceBank', mybet) == 1:
                    roulettearray = []
                    Spicebucks.spicebucks(bot, 'SpiceBank', 'plus', mybet)
                    bot.say(trigger.nick + " puts " + str(mybet) + " on " + str(mynumber) + " " + str(mycolor))
                    adjust_database_array(bot, 'casino', player, 'rouletteplayers', 'add')
                    set_database_value(bot,'casino','casinochannel',str(trigger.sender))
                    roulettearray.append(str(mybet))
                    roulettearray.append(str(mynumber))
                    roulettearray.append(mycolor)
                    testmsg = get_trigger_arg(bot, roulettearray,"list")
                    bot.notice("Your bet has been recorded", player)
                    set_database_value(bot, player, 'roulettearray', roulettearray)
                    numberofplayers = len(players)
                    if numberofplayers>=maxplayers:
                        runroulette(bot)
                    else:
                        bot.say("Spicebot will spin the wheel after " + str((maxplayers-numberofplayers)) + " more people have placed a bet")
                else:
                    bot.notice("You don't have enough Spicebucks to place that bet",player)

#-----Run roulette game
def runroulette(bot):
    maxwheel = int(get_database_value(bot,'casino','maxwheel')) or 24
    wheel = range(maxwheel + 1)
    colors = ['red', 'black']
    players = get_database_value(bot, 'casino', 'rouletteplayers') or []

    if not players == []:
        channel = get_database_value(bot,'casino','casinochannel')
        dispmsg = "Spicebot collects all bets"
        osd(bot, trigger.sender, 'say', dispmsg)
        winningnumber = spin(wheel)
        if winningnumber == 0:
            winningnumber == 1
        color = spin(colors)
        spicebankbalance=Spicebucks.bank(bot, 'SpiceBank') or 0
        mywinnings=0
        winners = []
        totalwon = 0
        displaymessage = get_trigger_arg(bot, players , "list")

        dispmsg = "Spicebot spins the wheel good luck to " + displaymessage
        osd(bot, trigger.sender, 'say', dispmsg)
        dispmsg = "The wheel stops on " + str(winningnumber) + " " + color
        osd(bot, trigger.sender, 'say', dispmsg)
        for player in players:
            mywinnings= 0
            mynumber = 0
            mycolor = ''
            playerarray =  get_database_value(bot, player, 'roulettearray') or ''
            if not playerarray == '':
                mybet =  get_trigger_arg(bot, playerarray, 1) or 0
                mybet = int(mybet)
                mynumber = get_trigger_arg(bot, playerarray, 2) or 0
                mynumber = int(mynumber)
                mycolor =  get_trigger_arg(bot, playerarray, 3) or ''

                if not mybet == 0:
                    if mynumber == winningnumber:
                        mywinnings=mybet * maxwheel
                    elif mycolor == color: # chance of choosing the same color is so high will set the payout to a fixed amount
                        newbet = int(mybet/2)
                        colorwinnings = mybet + newbet
                        mywinnings=mywinnings+colorwinnings
                    if mywinnings >=1:
                        bot.notice(("Roulette has ended and you have won " + str(mywinnings)),player)
                        if spicebankbalance < mywinnings:
                            Spicebucks.spicebucks(bot, player, 'plus', mywinnings)
                        else:
                            Spicebucks.transfer(bot, 'SpiceBank', player, mywinnings)
                            winners.append(player)
                            totalwon = totalwon + mywinnings
                        reset_database_value(bot, player, 'roulettearray')

        reset_database_value(bot, 'casino', 'rouletteplayers')
        reset_database_value(bot,'casino','counter')
        winnerarray = get_trigger_arg(bot,winners,'list')
        if len(winners)<1:
            dispmsg= "No winners this spin"
        elif len(winners)==1:
            dispmsg=  winnerarray + " won " + str(totalwon)
        else:
            dispmsg = "Winners: " + winnerarray + ". and total winnings were " + str(totalwon)
        osd(bot, trigger.sender, 'say', dispmsg)

#______Game 3 Lottery________
def lottery(bot,trigger, arg):
    lotterymax = int(get_database_value(bot,'casino','lotterymax')) or 25
    lotterytimeout = get_database_value(bot,'casino', 'lotterytimeout') #time between lottery drawings
    channel = trigger.sender
    player = trigger.nick
    bankbalance=Spicebucks.bank(bot,'SpiceBank')
    if bankbalance <=500:
        bankbalance=500
        Spicebucks.spicebucks(bot,'SpiceBank','plus',bankbalance)

    commandused = get_trigger_arg(bot, arg, 2) or 'nocommand'
    if not channel.startswith("#"):
        bot.notice(trigger.nick + ", lottery can only be used in a channel.", trigger.nick)
    else:
        if commandused == 'payout':
            bot.say("Current lottery jackpot is " + str(bankbalance) + ". Getting 4 number correct pays " + str(int(match4payout*bankbalance)) + " and getting 3 correct = " + str(int(bankbalance*match3payout)))
            success = 0
        else:
            picks = []
            success = 0

            picklen=len(arg)+1
            for i in range(0,picklen):
                picker = get_trigger_arg(bot, arg, i)
                if picker.isdigit():
                    picks.append(int(picker))

            if len(picks)!=5:
                bot.notice(('You must enter 5 lottery numbers from 1 to ' + str(lotterymax) + ' to play.'),player)
                success = 0
            else:
                success = 1
            if success == 1:
                pickstemp = picks
                picks = []
                for pick in pickstemp:
                    if pick not in picks:
                        picks.append(pick)
                if len(picks) < 5:
                    bot.notice('You must choose 5 different numbers.',player)
                    success = 0
                if success == 1:
                    valid=1
                    for pick in picks:
                        if(pick > lotterymax or pick < 1):
                            valid = 0
                    if valid == 0:
                        bot.notice(('One of the numbers you entered is not within the valid range of 1 to ' + str(lotterymax)),player)
                    else:
                        lottoplayers= get_database_value(bot,'casino','lottoplayers') or []
                        if player in lottoplayers:
                            bot.notice("You are already in this drawing",player)
                        else:
                            if Spicebucks.transfer(bot, player, 'SpiceBank', 1) == 1:
                                bot.say(player + " bets on the numbers " + str(picks))
                                set_database_value(bot,player,'picks', picks)
                                adjust_database_array(bot,'casino',player, 'lottoplayers','add')
                                set_database_value(bot,'casino','lotterychanel',trigger.sender)
                                nextlottery = get_timesince(bot,'casino','lastlottery')
                                bot.notice("Next lottery drawing in " + str(hours_minutes_seconds((lotterytimeout-nextlottery))),player)
                            else:
                                bot.notice('You dont have enough Spicebucks',player)

##_______Lottery drawing
def lotterydrawing(bot):
    lotterymax = int(get_database_value(bot,'casino','lotterymax')) or 25
    bankbalance=Spicebucks.bank(bot,'SpiceBank')
    nextlottery = get_timesince(bot,'casino','lastlottery')
    lotterytimeout=get_database_value(bot,'casino', 'lotterytimeout')

    channel = get_database_value(bot,'casino','lotterychanel')
    lotteryplayers = get_database_value(bot, 'casino','lottoplayers')
    lotterywinners =[]
    totalwon = 0
    bigwinner = ''
    bigwinpayout=0

    #if get_database_array_total(bot, 'casino','lottoplayers') <1:
    #    msg= "No one entered this lottery. Next lottery drawing will be in " + str(hours_minutes_seconds(lotterytimeout-nextlottery))
    #    osd(bot, channel, 'say', msg)
    #else:
    if get_database_array_total(bot, 'casino','lottoplayers') >0:
        if bankbalance <=500:
            bankbalance=500
            set_database_value(bot,'SpiceBank', 'spicebucks_bank', bankbalance)

        winningnumbers = random.sample(range(1,lotterymax), 5)

        msg ='The winning numbers are ' + str(winningnumbers)
        osd(bot, channel, 'say', msg)
        for player in lotteryplayers:
            correct = 0
            picks = get_database_value(bot,player,'picks') or []
            for pick in picks:
                if pick in winningnumbers:
                    correct = correct + 1
            payout = 0
            if correct == 1:
                payout = match1payout
            elif correct == 2:
                payout = match2payout
            elif correct == 3:
                payout = int(match3payout*bankbalance)
            elif correct == 4:
                payout = int(match4payout*bankbalance)
            elif correct == 5:
                payout = bankbalance

            if payout>bankbalance:
                Spicebucks.spicebucks(bot,'SpiceBank','plus',payout)
            if payout > 0:
                bot.notice("You won " + str(payout) + " in the lottery drawing",player)
                Spicebucks.transfer(bot, 'SpiceBank', player, payout)
                lotterywinners.append(player)
                totalwon = totalwon + payout
                if payout > bigwinpayout:
                    bigwinpayout = payout
                    bigwinner = player
                bankbalance=Spicebucks.bank(bot,'SpiceBank')
            else:
                bot.notice('You are not a lottery winner',player)

        if totalwon >0:
            lottowinners = get_trigger_arg(bot, lotterywinners, "list")
            if len(lotterywinners) >1:
                msg ="Lottery winners: " + lottowinners + ", and the big winner was " +bigwinner + " winning " + str(bigwinpayout) + " in this drawing"
            else:
                msg = lottowinners + " won " + str(bigwinpayout) + " in this drawing"
            osd(bot, channel, 'say', msg)
        else:
            msg="No one won this drawing."
            osd(bot, channel, 'say', msg)
    reset_database_value(bot, 'casino','lottoplayers')

#____Game 4 Blackjack___
def blackjack(bot,trigger,arg):
    minbet=30
    blackjackpayout = 2
    beatdealerpayout = 2
    payouton21 = 1
    mychoice = get_trigger_arg(bot, arg, 2) or 'nocommand'
    mychoice2 = get_trigger_arg(bot, arg, 3) or 'nocommand'
    if mychoice == 'nocommand':
        bot.say("Use .gamble blackjack deal <bet> amount to start a new game")

    else:
        if bot.nick == "Spicebotdev":
            deck = [2, 3, 4, 5, 6, 10, 10, 10, 'J', 'A']*4
        else:
            deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4
        myhand = []
        dealerhand = []
        player=trigger.nick
        payout = 0
        if(mychoice == 'deal' or mychoice == 'start' or mychoice == '1'):
            if mychoice2 == 'nocommand':
                bot.notice("Please enter an amount you wish to bet", player)
            else:
                if not mychoice2.isdigit():
                    bot.notice(('Please bet a number between ' + str(minbet) + ' and ' + str(maxbet)),player)
                else:
                    mybet=int(mychoice2)
                    if (mybet<minbet or mybet>maxbet):
                        bot.notice(('Please bet an amount between ' + str(minbet) + ' and ' + str(maxbet)),player)
                    else:
                        if not get_database_value(bot, player, 'mybet')==0:
                            bot.notice("You already have a game start. Use hit or stand to finish the current game.",player)
                        else:
                            if Spicebucks.transfer(bot, player, 'SpiceBank', mybet) == 1:
                                myhand = deal(bot,deck, 2)
                                dealerhand = deal(bot,deck, 2)
                                bot.say(player + ' has a ' + str(myhand[0]) + ' and a ' + str(myhand[1]) + ' Spicebot has a ' + str(dealerhand[1]) + ' showing.')
                                myscore = blackjackscore(bot,myhand)
                                dealerscore = blackjackscore(bot,dealerhand)
                                payout = mybet
                                if myscore == 21:
                                    payout=payout + (mybet*blackjackpayout)
                                    bot.say(player + ' got blackjack and wins ' + str(payout))
                                    Spicebucks.spicebucks(bot, player, 'plus', payout)
                                else:

                                    #update hand in the database
                                    set_database_value(bot, player, 'myhand', myhand)
                                    set_database_value(bot, player, 'dealerhand', dealerhand)
                                    set_database_value(bot, player, 'mybet', mybet)
                                    bot.notice(" You can say'.gamble blackjack hit' to take a card or '.gamble blackjack stand' to finish the game",player)
                            else:
                                bot.notice('You do not have enough spicebucks.',player)
        elif mychoice == 'hit' or mychoice == '2':
            myhand =  get_database_value(bot,player, 'myhand') or 0
            payout = get_database_value(bot,player, 'mybet') or 0
            if (myhand == [] or myhand ==0):
                bot.say('Use deal to start a new game')
            else:
                if len(myhand)>=6:
                    payment = payout+(int(payout/2))
                    bot.say(player + str(payment) + " wins for having more then 5 cards.")
                    Spicebucks.spicebucks(bot, player, 'plus', payout)
                    blackjackreset(bot,player)

                else:
                    bot.say("Player hand before hit: " + str(myhand))
                    playerhitlist = ''
                    hitcard=deal(bot,deck, 1)
                    playerhits=hitcard[0]

                    myhand.append(playerhits)
                    bot.say("Player hand after hit: " + str(myhand))
                    myscore = blackjackscore(bot,myhand)

                    if myscore <= 21:
                        set_database_value(bot, player, 'myhand', myhand)
                        bot.say(player + " takes a hit and a gets a " + str(playerhits) + " " + player + "'s score is now " + str(myscore))
                    else:
                        bot.say(player + ' got ' + str(playerhits) + ' busted and gets nothing')
                        blackjackreset(bot,player)

        elif mychoice == 'check':
            target = mychoice2
            if targetcheck(bot, target,player)==0:
                bot.say("Target not found.")
            else:
                myhand =  get_database_value(bot,target, 'myhand') or 0
                dealerhand = get_database_value(bot,target, 'dealerhand') or 0
                bot.say(target + ' has ' + str(myhand) + ' Spicebot has ' + str(dealerhand))

        elif mychoice == 'double' or mychoice == '4':
            myhand = get_database_value(bot,player, 'myhand') or 0
            payout = get_database_value(bot,player, 'mybet') or 0
            dealerhand = get_database_value(bot,player, 'dealerhand') or 0
            if (myhand == [] or myhand ==0):
                bot.say('Use deal to start a new game')
            else:
                if len(myhand) == 2:
                    mybet=payout+payout
                    set_database_value(bot,player, 'mybet', mybet)
                    playerhitlist = ''

                    playerhits=deal(bot,deck, 1)
                    playerhits=playerhits[0]
                    myhand.append(playerhits)
                    set_database_value(bot,player, 'myhand', myhand)
                    bot.say(player + " doubles down and gets " + str(playerhits))
                    blackjackstand(bot,player,myhand,dealerhand,mybet)



        elif mychoice == 'stand' or mychoice == '3':
            myhand =  get_database_value(bot,player, 'myhand') or 0
            dealerhand = get_database_value(bot,player, 'dealerhand') or 0
            payout = get_database_value(bot,player, 'mybet') or 0
            blackjackstand(bot,player,myhand,dealerhand,payout)

        elif mychoice == 'payout':
            bot.say("Getting blackjack pays 2x, getting 21 pays 1x, beating Spicebot pays 1/2 your bet.")

        else:
            bot.say('Choose an option: deal, hit, or stand')

#__________________________Shared Functions____________________
def spin(wheel):
    random.seed()
    selected=random.randint(0,(len(wheel)-1))
    reel=wheel[selected]
    return reel

def deal(bot, deck, cardcount):
    #choose a random card from a deck and remove it from deck
    hand = []

    for i in range(cardcount):
        card = get_trigger_arg(bot, deck,'random')

        hand.append(card)
    return hand

def blackjackstand(bot,player,myhand,dealerhand,payout):
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']*4
    if (myhand == [] or myhand ==0):
        bot.say('Use deal to start a new game')
    else:
        myscore = blackjackscore(bot,myhand)

        dealerscore = blackjackscore(bot,dealerhand)
        dealerwins=''
        if myscore == 21:
            payout=payout + payout
            bot.say(player + ' got blackjack and is a winner of ' + str(payout))
            Spicebucks.spicebucks(bot, player, 'plus', payout)
        elif myscore > 21:
            bot.say(player + ' busted and gets nothing')
        elif myscore < 21:
            dealerhitlist = ''
            while dealerscore < 18:
                dealerhits=deal(bot,deck, 1)
                dealerhits=dealerhits[0]
                dealerhitlist=dealerhitlist + ' ' + str(dealerhits)
                dealerhand.append(dealerhits)
                dealerscore=blackjackscore(bot,dealerhand)
            if not dealerhitlist == '':
                hitlist=int(len(dealerhitlist)/2) #count spaces
                if hitlist>1:
                    bot.say('Spicebot takes ' + str((hitlist)) + ' hits and gets' + dealerhitlist)
                else:
                    bot.say('Spicebot takes a hit and gets a' + dealerhitlist)
            showdealerhand = ''

            for i in dealerhand:
                showdealerhand = showdealerhand + " " + str(i)

            if dealerscore > 21:
                payout=payout + int((payout/2))
                Spicebucks.spicebucks(bot, player, 'plus', payout)
                bot.say("Spicebot had " + showdealerhand + " busts")
                bot.say(player + ' wins ' + str(payout))
            elif dealerscore == 21:
                bot.say("Spicebot has " + showdealerhand + " and wins")
            elif dealerscore < myscore:
                payout=payout + int((payout/2))
                Spicebucks.spicebucks(bot, player, 'plus', payout)
                bot.say("Spicebot had " + showdealerhand + " " + player + " wins " + str(payout))
            elif dealerscore > myscore:
                bot.say("Spicebot had " + showdealerhand + " and wins")
            elif dealerscore == myscore:
                Spicebucks.spicebucks(bot, player, 'plus', payout)
                bot.say('It is a draw and ' + player + ' gets ' + str(payout))
            else:
                bot.say('No games found say .gamble blackjack deal to start a new game')
        blackjackreset(bot,player)

def blackjackscore(bot,hand):
    myscore = 0
    #hand=get_trigger_arg(bot,hand,'list')
    i=0
    myhand= []
    handlen = len(hand)
    for i in range(0,handlen):
        card = get_trigger_arg(bot, hand, i)
        if card.isdigit():
            myscore=myscore+int(card)
        elif(card == 'J' or card == 'Q' or card == 'K'):
            myscore = myscore + 10
        elif card=='A':
            myscore = myscore + 11
    if myscore > 21:
       # bot.say("Player score: " + str(myscore))
        if 'A' in hand:
            myhand = hand.replace('A','1')
            newscore = blackjackscore(bot,myhand)
            return newscore
        else:
           # bot.say("Return player score : " + str(myscore))
            return myscore
    else:
        return myscore
    return myscore

def blackjackreset(bot,player):
    reset_database_value(bot,player, 'myhand')
    reset_database_value(bot,player, 'dealerhand')
    reset_database_value(bot,player, 'mybet')

@sopel.module.interval(10)
def countdown(bot):
    now = time.time()
    currentsetting = get_database_value(bot,'casino','counter')
    roulettetimediff = get_timesince(bot,'casino','countertimer')
    lotterytimediff= get_timesince(bot,'casino','lastlottery')
    lotterytimeout = get_database_value(bot,'casino', 'lotterytimeout')
    if currentsetting == 'roulette':
        if roulettetimediff>=roulettetimeout:
            runroulette(bot)
    if lotterytimediff>=lotterytimeout and lotterytimeout>=10:
        set_database_value(bot,'casino','lastlottery',now)
        lotterydrawing(bot)

def admincommands(bot,trigger,arg):
    player=trigger.nick
    subcommand=get_trigger_arg(bot, arg, 2) or 'nocommand'
    commandvalue = get_trigger_arg(bot, arg, 3) or 'nocommand'
    if subcommand=='slotadd':
        adjust_database_array(bot,'casino',commandvalue,'slotwheel','add')
        bot.notice(commandvalue + " added to slot wheel.",trigger.nick)
    elif subcommand=='slotdefault':
        wheel = ['MODEM', 'BSOD', 'RAM', 'CPU', 'RAID', 'VLANS', 'PATCH', 'WIFI', 'CPU', 'CLOUD', 'VLANS', 'AI','DARKWEB','BLOCKCHAIN','PASSWORD']
        set_database_value(bot,'casino','slotwheel',wheel)
        set_database_value(bot, 'casino','slotkeyword','BSOD')
        bot.notice("Slot wheel set to defaults.",trigger.nick)
    elif subcommand=='slotremove':
        existingwheel = get_database_value(bot,'casino','slotwheel')
        if commandvalue in existingwheel:
            adjust_database_array(bot,'casino',commandvalue,'slotwheel','del')
            bot.notice(commandvalue + " removed from slot wheel.",trigger.nick)
    elif subcommand =='slotkeyword':
        existingwheel = get_database_value(bot,'casino','slotwheel')
        if commandvalue in existingwheel:
            set_database_value(bot, 'casino','slotkeyword',commandvalue)
            bot.notice( "Slot keyword '" + commandvalue + "' added to slot wheel.",trigger.nick)
    elif subcommand == 'slotlist':
        slotlist=get_database_value(bot,'casino','slotwheel')
        listslots=get_trigger_arg(bot,slotlist,'list')
        bot.notice("Slot wheel: " + listslots,player)

    elif subcommand == 'roulettereset':
        reset_database_value(bot, 'casino', 'rouletteplayers')
        reset_database_value(bot,'casino','counter')
        bot.notice("Stats reset for roulette",trigger.nick)
    elif subcommand == 'rouletteend':
        set_database_value(bot,'casino','casinochannel',str(trigger.sender))
        runroulette(bot)
    elif subcommand=='roulettemax':
        if commandvalue.isdigit():
            wheelmax=int(commandvalue)
            if wheelmax >=10:
                set_database_value(bot,'casino','maxwheel',wheelmax)
                bot.notice("Roulette wheel max set to " + str(wheelmax),trigger.nick)
            else:
                bot.notice("Enter a number larger then 10",trigger.nick)
        else:
            bot.notice("Please enter a valid number",trigger.nick)
    elif subcommand == 'lotterymax':
        maxvalue = commandvalue
        if maxvalue.isdigit():
            maxvalue=int(maxvalue)
            if maxvalue>=10:
                set_database_value(bot,'casino','lotterymax',maxvalue)
                bot.notice("Lottery max set to " + str(maxvalue),player)
            else:
                bot.notice("Please enter a number large then 10",player)
        else:
            bot.notice("Please enter a valid number",player)
    elif subcommand == 'lotteryend':
        lotterydrawing(bot)
    elif subcommand == 'lotterytime':
        if commandvalue.isdigit():
            lotterytime = int(commandvalue)
            if lotterytime >=10:
                set_database_value(bot,'casino', 'lotterytimeout',lotterytime)
                bot.notice("Lottery time out is set " + str(lotterytime) + " seconds",trigger.nick)
            else:
                bot.notice("Please enter a number larger then 10",player)
        else:
            bot.notice("Please enter a valid number",trigger.nick)

    elif subcommand == 'blackjackset':
        if targetcheck(bot, commandvalue,player)==0:
            bot.say("Target not found.")
        else:
            reset_database_value(bot,commandvalue, 'myhand')
            reset_database_value(bot,commandvalue, 'dealerhand')
            reset_database_value(bot,commandvalue, 'mybet')
            bot.notice("Blackjack reset for: " + commandvalue,trigger.nick)
