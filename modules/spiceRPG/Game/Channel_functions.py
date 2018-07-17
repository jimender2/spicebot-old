"""
Channels
"""


def rpg_command_channels(bot,rpg,trigger):
    rpg.channel_current = trigger.sender
    if not rpg.channel_current.startswith("#"):
        rpg.channel_priv = 1
        rpg.channel_real = 0
    else:
        rpg.channel_priv = 0
        rpg.channel_real = 1
    rpg.service = bot.nick
    rpg.channel_list = []
    for channel in bot.channels:
        rpg.channel_list.append(channel)
    return rpg
