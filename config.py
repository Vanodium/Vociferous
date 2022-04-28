import discord


class en_user_messages():
    # сообщения пользователю
    def song_preparing():
        return "Preparing the song..."
    
    def stream_preparing():
        return "Preparing the radio..."
    
    def playing():
        return "Playing the song"

    def song_paused():
        return "Song is paused"

    def song_resumed():
        return "Song is resumed"

    def song_already_playing():
        return "Song is already playing"

    def downloading_error():
        return "Got ishues with downloading"

    def song_ready():
        return "Ready to play!"
    
    def wrong_genre():
        return "Sorry, we don't have this genre"

    def more_info():
        return "Vociferous - musical discord bot since 2022. Made by 𝔙𝔞𝔫𝔬𝔡𝔦𝔲𝔪#7923"
    
    def give_role(role):
        return "Now you are " + role + '!'
    
    def remove_role(role):
        return "Now you are not " + role + ' (('

    def wrong_remove_role():
        return "You can't remove role u don't have"
    
    def already_have_role():
        return "You already have this role"

    def help(status=True):
        # задаём цвет сообщения
        if status:
            embed = discord.Embed(
                color=discord.Color.blurple()
                )
            # заголовок
            embed.set_author(name='Help')
        else:
            embed = discord.Embed(
                color=discord.Color.red()
                )
            # заголовок
            embed.set_author(name='Wrong command. Maybe u mean these?')
        # описание команд
        embed.add_field(name='!help', value='Get help with the commands', inline=True)
        embed.add_field(name='!stream <genre>', value='Streams any genre in radio mode', inline=True)
        embed.add_field(name='!play <link>', value='Plays any song from YouTube', inline=True)
        embed.add_field(name='!play/!pause', value='Plays/pauses song', inline=True)
        embed.add_field(name='!role <genre>',
            value='Get role by your favourite genres!\nRoles: melomaniac, rocker, EDMer, rapper, classician, bluesman', inline=True)
        embed.add_field(name='!role <genre> remove', value='Remove role by genre', inline=True)
        embed.add_field(name='!FAQ', value='More info about us', inline=True)
        return embed
        

# чат, который читает бот
bot_txtchannel_id = 961626634472030349
# чат, в котором бот выдаёт роли
bot_roleschannel_id = 961626910939553792
# чат, в котором говорит бот
bot_voicechannel_id = 960538088629747757

music_folder = 'downloads'
radiostations_base = 'db/stations.db'
