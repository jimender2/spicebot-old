import requests
import json
from sopel.module import commands, example, NOLIMIT
from HTMLParser import HTMLParser
import re
import random


@commands('trivia', 'tt')
def trivia(bot, trigger):
    if not bot.db.get_nick_value(bot.nick, 'trivia_status'):
        bot.db.set_nick_value(bot.nick, 'trivia_status', False)
    if trigger.group(2) == "on":
        bot.db.set_nick_value(bot.nick, 'trivia_status', True)
        get_trivia(bot)
    elif trigger.group(2) == "off":
        bot.db.set_nick_value(bot.nick, 'trivia_status', False)
    else:
        get_trivia(bot)


@commands('answer', 'a')
def trivia_answer(bot, trigger):
    check_values(bot, trigger.nick)
    guess = trigger.group(2)
    answer = bot.db.get_nick_value(bot.nick, 'trivia_answer')
    if answer:
        answer = answer.lower()
    if guess:
        guess = guess.lstrip().rstrip().lower()
    if guess == "help?":
        bot.say("? for hint, ??? for answer")
    elif not answer:
        bot.say("You need to ask a question!")
    elif not guess:
        bot.say("Answer: %s" % (re.sub('[a-zA-Z0-9]', '*', answer)))
    elif guess == "?":
        hint = ""
        for x in answer:
            if random.randint(0, 100) >= 70:
                hint += x
            else:
                hint += "*"
        bot.say(hint)
        hints = bot.db.get_nick_value(trigger.nick, 'trivia_hints')
        bot.db.set_nick_value(trigger.nick, 'trivia_hints', hints + 1)
    elif guess == "???":
        bot.say(answer)
        bot.db.set_nick_value(bot.nick, 'trivia_answer', None)
        if bot.db.get_nick_value(bot.nick, 'trivia_status'):
            get_trivia(bot)
    elif guess.lower() == answer:
        bot.say("Correct!")
        bot.db.set_nick_value(bot.nick, 'trivia_answer', None)
        score = bot.db.get_nick_value(trigger.nick, 'trivia_score')
        bot.db.set_nick_value(trigger.nick, 'trivia_score', score + 1)
        bot.say("%s has %d points!" % (trigger.nick, bot.db.get_nick_value(trigger.nick, 'trivia_score')))
        if bot.db.get_nick_value(bot.nick, 'trivia_status'):
            get_trivia(bot)
    else:
        bot.say("Nope!")
        wrong = bot.db.get_nick_value(trigger.nick, 'trivia_wrong')
        bot.db.set_nick_value(trigger.nick, 'trivia_wrong', wrong + 1)


@commands('score')
def trivia_score(bot, trigger):
    if not trigger.group(2):
        nick = trigger.nick
    else:
        nick = trigger.group(2).lstrip().rstrip()
    check_values(bot, nick)
    score = bot.db.get_nick_value(nick, 'trivia_score')
    wrong = bot.db.get_nick_value(nick, 'trivia_wrong')
    hints = bot.db.get_nick_value(nick, 'trivia_hints')
    bot.say("%s has %d points, has had %d wrong answers, and has used %d hints!" % (nick, score, wrong, hints))


def get_trivia(bot):
    header = {"User-Agent": "Syrup/1.0"}
    response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple", headers=header)
    data = response.json()
    if data['response_code'] != 0:
        bot.say("Error getting question, sorry.")
    g_question = data["results"][0]
    answer = HTMLParser().unescape(g_question["correct_answer"]).lower()
    old_answer = bot.db.get_nick_value(bot.nick, 'trivia_answer')
    if old_answer:
        bot.say("The previous answer was: %s" % (old_answer))
    bot.db.set_nick_value(bot.nick, 'trivia_answer', answer)
    question = HTMLParser().unescape(g_question["question"])
    starred_answer = re.sub('[a-zA-Z0-9]', '*', answer)
    bot.say("Question: %s" % (question))
    bot.say("Answer: %s" % (starred_answer))


def check_values(bot, nick):
    if not bot.db.get_nick_value(nick, 'trivia_score'):
        bot.db.set_nick_value(nick, 'trivia_score', 0)
    if not bot.db.get_nick_value(nick, 'trivia_wrong'):
        bot.db.set_nick_value(nick, 'trivia_wrong', 0)
    if not bot.db.get_nick_value(nick, 'trivia_hints'):
        bot.db.set_nick_value(nick, 'trivia_hints', 0)
    return
