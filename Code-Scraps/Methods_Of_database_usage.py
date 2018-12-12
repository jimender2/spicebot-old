"""
Sopel methods
"""

# Get
database_value = bot.db.get_nick_value(nick, databasecolumn) or 0

# Set
bot.db.set_nick_value(nick, databasecolumn, value)

# reset
bot.db.set_nick_value(nick, databasecolumn, None)


"""
Advanced Methods
"""


# Get a value
def get_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    database_value = bot.db.get_nick_value(nick, databasecolumn) or 0
    return database_value


# set a value
def set_database_value(bot, nick, databasekey, value):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, value)


# set a value to None
def reset_database_value(bot, nick, databasekey):
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, None)


# add or subtract from current value
def adjust_database_value(bot, nick, databasekey, value):
    oldvalue = get_database_value(bot, nick, databasekey) or 0
    databasecolumn = str(databasekey)
    bot.db.set_nick_value(nick, databasecolumn, int(oldvalue) + int(value))


# array stored in database length
def get_database_array_total(bot, nick, databasekey):
    array = get_database_value(bot, nick, databasekey) or []
    entriestotal = len(array)
    return entriestotal


# array stored in database, add or remove elements
def adjust_database_array(bot, nick, entries, databasekey, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    adjustarray = get_database_value(bot, nick, databasekey) or []
    adjustarraynew = []
    for x in adjustarray:
        adjustarraynew.append(x)
    reset_database_value(bot, nick, databasekey)
    adjustarray = []
    if adjustmentdirection == 'add':
        for y in entries:
            if y not in adjustarraynew:
                adjustarraynew.append(y)
    elif adjustmentdirection == 'del':
        for y in entries:
            if y in adjustarraynew:
                adjustarraynew.remove(y)
    for x in adjustarraynew:
        if x not in adjustarray:
            adjustarray.append(x)
    if adjustarray == []:
        reset_database_value(bot, nick, databasekey)
    else:
        set_database_value(bot, nick, databasekey, adjustarray)


"""
Individual user dicts saved in database
"""


# Database Users
def get_user_dict(bot, dynamic_class, nick, dictkey):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    returnvalue = 0

    # check if nick has been pulled from db already
    if nick not in dynamic_class.userdb.list:
        dynamic_class.userdb.list.append(nick)
        nickdict = get_database_value(bot, nick, dynamic_class.default) or dict()
        createuserdict = str("dynamic_class.userdb." + nick + " = nickdict")
        exec(createuserdict)
    else:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)

    if dictkey in nickdict.keys():
        returnvalue = nickdict[dictkey]
    else:
        nickdict[dictkey] = 0
        returnvalue = 0

    return returnvalue


# set a value
def set_user_dict(bot, dynamic_class, nick, dictkey, value):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = value


# reset a value
def reset_user_dict(bot, dynamic_class, nick, dictkey):
    currentvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    if dictkey in nickdict:
        del nickdict[dictkey]


# add or subtract from current value
def adjust_user_dict(bot, dynamic_class, nick, dictkey, value):
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    if not str(oldvalue).isdigit():
        oldvalue = 0
    nickdict = eval('dynamic_class.userdb.' + nick)
    nickdict[dictkey] = oldvalue + value


# Save all database users in list
def save_user_dicts(bot, dynamic_class):

    # check that db list is there
    if not hasattr(dynamic_class, 'userdb'):
        dynamic_class.userdb = class_create('userdblist')
    if not hasattr(dynamic_class.userdb, 'list'):
        dynamic_class.userdb.list = []

    for nick in dynamic_class.userdb.list:
        if not hasattr(dynamic_class.userdb, nick):
            nickdict = dict()
        else:
            nickdict = eval('dynamic_class.userdb.' + nick)
        set_database_value(bot, nick, dynamic_class.default, nickdict)


# add or subtract from current value
def adjust_user_dict_array(bot, dynamic_class, nick, dictkey, entries, adjustmentdirection):
    if not isinstance(entries, list):
        entries = [entries]
    oldvalue = get_user_dict(bot, dynamic_class, nick, dictkey)
    nickdict = eval('dynamic_class.userdb.' + nick)
    if not isinstance(oldvalue, list):
        oldvalue = []
    for x in entries:
        if adjustmentdirection == 'add':
            if x not in oldvalue:
                oldvalue.append(x)
        elif adjustmentdirection == 'del':
            if x in oldvalue:
                oldvalue.remove(x)
    nickdict[dictkey] = oldvalue


"""
Current Method all users, kept in bot.memory

* longevity can be long or temp, temp is wiped at bot reboot, long is saved to the database

* sorting key is designed to organize functionality, claims, duels, etc would all be sorted together

* use key is the actual value you are using

"""


# get values from other bots
def get_nick_value_api(bot, botname, nick, longevity, sortingkey, usekey):
    try:
        if longevity == 'long':
            botvaltime = bot.memory["altbots"][botname]["users"][nick][sortingkey][usekey]["value"]
        elif longevity == 'temp':
            botvaltime = bot.memory["altbots"][botname]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"]
    except Exception as e:
        botvaltime = None
    return botvaltime


# get nick value from bot.memory
def get_nick_value(bot, nick, longevity, sortingkey, usekey):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Get the value
    if longevity == 'long':
        if "value" not in bot.memory["botdict"]["users"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = None
        if "timestamp" not in bot.memory["botdict"]["users"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = 0
        return bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"]
    elif longevity == 'temp':
        if "value" not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = None
        if "timestamp" not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = 0
        return bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"]


def adjust_nick_value(bot, nick, longevity, sortingkey, usekey, value):
    oldvalue = get_nick_value(bot, nick, longevity, sortingkey, usekey) or 0
    set_nick_value(bot, nick, longevity, sortingkey, usekey, int(oldvalue) + int(value))


# set nick value in bot.memory
def set_nick_value(bot, nick, longevity, sortingkey, usekey, value):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Se the value
    currtime = time.time()
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = value
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = currtime
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = value
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = currtime


# set nick value in bot.memory
def reset_nick_value(bot, nick, longevity, sortingkey, usekey):

    # if str(bot.nick).endswith("dev"):
    #    usekey = usekey + "_dev"

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify sortingkey exists
    if longevity == 'long':
        if sortingkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][sortingkey] = dict()
    elif longevity == 'temp':
        if sortingkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey] = dict()

    # Verify usekey exists
    if longevity == 'long':
        if usekey not in bot.memory["botdict"]["users"][nick][sortingkey].keys():
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["users"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["users"][nick][sortingkey][usekey]
            bot.memory["botdict"]["users"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = oldvalue
    elif longevity == 'temp':
        if usekey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
        if not isinstance(bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey], dict):
            oldvalue = bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey] = dict()
            bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = oldvalue

    # Reset the value
    currtime = time.time()
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["value"] = None
        bot.memory["botdict"]["users"][nick][sortingkey][usekey]["timestamp"] = currtime
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["value"] = None
        bot.memory["botdict"]["tempvals"]["uservals"][nick][sortingkey][usekey]["timestamp"] = currtime


def adjust_nick_array(bot, nick, longevity, sortingkey, usekey, values, direction):

    if not isinstance(values, list):
        values = [values]

    oldvalues = get_nick_value(bot, nick, longevity, sortingkey, usekey) or []

    # startup entries
    if direction == 'startup':
        if longevity == 'long':
            if oldvalues == []:
                direction == 'add'
            else:
                return
        elif longevity == 'temp':
            if oldvalues == []:
                direction == 'add'
            else:
                return

    # adjust
    for value in values:
        if longevity == 'long':
            if direction == 'add':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction == 'startup':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction in ['del', 'remove']:
                if value in oldvalues:
                    oldvalues.remove(value)
        elif longevity == 'temp':
            if direction == 'add':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction == 'startup':
                if value not in oldvalues:
                    oldvalues.append(value)
            elif direction in ['del', 'remove']:
                if value in oldvalues:
                    oldvalues.remove(value)

    set_nick_value(bot, nick, longevity, sortingkey, usekey, oldvalues)
