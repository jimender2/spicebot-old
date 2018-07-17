"""
Users
"""

from .Database_adjust import *


def rpg_command_users(bot,rpg):
    rpg.opadmin,rpg.owner,rpg.chanops,rpg.chanvoice,rpg.botadmins,rpg.users_current = [],[],[],[],[],[]

    for user in bot.users:
        rpg.users_current.append(str(user))
    adjust_database_array(bot, 'channel', rpg.users_current, 'users_all', 'add')
    rpg.users_all = get_database_value(bot, 'channel', 'users_all') or []

    for user in rpg.users_current:

        if user in bot.config.core.owner:
            rpg.owner.append(user)

        if user in bot.config.core.admins:
            rpg.botadmins.append(user)
            rpg.opadmin.append(user)

        for channelcheck in bot.channels:
            try:
                if bot.privileges[channelcheck][user] == OP:
                    rpg.chanops.append(user)
                    rpg.opadmin.append(user)
            except KeyError:
                dummyvar = 1
            try:
                if bot.privileges[channelcheck][user] == VOICE:
                    rpg.chanvoice.append(user)
            except KeyError:
                dummyvar = 1

    return rpg
