from commands import (
    bot_commands,
)

def load_the_commands(client, tree, bot):
    bot_commands.define_commands(tree, bot)