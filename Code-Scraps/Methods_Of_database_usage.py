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
"""


# get nick value from bot.memory
def get_nick_value(bot, nick, secondarykey, longevity='long', mainkey='unsorted'):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # Verify secondarykey exists
    if longevity == 'long':
        if secondarykey not in bot.memory["botdict"]["users"][nick][mainkey].keys():
            return None
        else:
            return bot.memory["botdict"]["users"][nick][mainkey][secondarykey]
    elif longevity == 'temp':
        if secondarykey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey].keys():
            return None
        else:
            return bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]


# set nick value in bot.memory
def set_nick_value(bot, nick, secondarykey, value, longevity='long', mainkey='unsorted'):

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # set
    if longevity == 'long':
        bot.memory["botdict"]["users"][nick][mainkey][secondarykey] = value
    elif longevity == 'temp':
        bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] = value


# adjust a list of entries in bot.memory
def adjust_nick_array(bot, nick, secondarykey, values, direction, longevity='long', mainkey='unsorted'):

    if not isinstance(values, list):
        values = [values]

    # verify nick dict exists
    if longevity == 'long':
        if nick not in bot.memory["botdict"]["users"].keys():
            bot.memory["botdict"]["users"][nick] = dict()
    elif longevity == 'temp':
        if nick not in bot.memory["botdict"]["tempvals"]["uservals"].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick] = dict()

    # Verify mainkey exists
    if longevity == 'long':
        if mainkey not in bot.memory["botdict"]["users"][nick].keys():
            bot.memory["botdict"]["users"][nick][mainkey] = dict()
    elif longevity == 'temp':
        if mainkey not in bot.memory["botdict"]["tempvals"]["uservals"][nick].keys():
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey] = dict()

    # verify array exists
    if longevity == 'long':
        if secondarykey not in bot.memory["botdict"]["users"][nick][mainkey]:
            bot.memory["botdict"]["users"][nick][mainkey][secondarykey] = []
    elif longevity == 'temp':
        if secondarykey not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey]:
            bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] = []

    # startup entries
    if direction == 'startup':
        if longevity == 'long':
            if bot.memory["botdict"]["users"][nick][mainkey][secondarykey] == []:
                direction == 'add'
            else:
                return
        elif longevity == 'temp':
            if bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey] == []:
                direction == 'add'
            else:
                return

    # adjust
    for value in values:
        if longevity == 'long':
            if direction == 'add':
                if value not in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].append(value)
            elif direction == 'startup':
                if value not in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].append(value)
            elif direction in ['del', 'remove']:
                if value in bot.memory["botdict"]["users"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["users"][nick][mainkey][secondarykey].remove(value)
        elif longevity == 'temp':
            if direction == 'add':
                if value not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].append(value)
            elif direction == 'startup':
                if value not in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].append(value)
            elif direction in ['del', 'remove']:
                if value in bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey]:
                    bot.memory["botdict"]["tempvals"]["uservals"][nick][mainkey][secondarykey].remove(value)