import discord
import sheet

KB = discord.Client()


@KB.event
async def on_ready():
    '''
    Triggered when server is just starting up
    '''
    print('Logged on as {0}!'.format(KB.user))


@KB.event
async def on_message(message):
    '''
    on_message
        1. Only respones if @Kiosk Bot is mentioned
    
    Command List:
        1. check in
        Gives 'on shift' role
        2. check out
        Removes 'on shift' role

    '''
    
    if message.author == KB.user:
        '''
        Reading its own message
        '''
        return

    if discord.utils.get(message.guild.members, name='Kiosk Bot') not in message.mentions or len(message.mentions) != 1:
        '''
        Ignore messages without mentioning @Kiosk Bot
        '''
        return
    
    guild = message.guild
    member = message.author
    
    # when check in
    if 'check in' in message.content:
        role = discord.utils.get(guild.roles, name='on shift')
        if role is not None:
            # if member is not on shift yet
            if role not in member.roles:
                try:
                    print(f'{member} is checking in..')
                    sheet.check_in_staff(member.display_name)
                    await member.add_roles(role)
                    await message.channel.send(f'{member.mention} you\'ve been checked in')
                except Exception as e:
                    print(e)
                    print('Check in fail')
                    await message.channel.send('Check in fail :(')
            # if member is already on shift
            else:
                await message.channel.send(f'{member.mention} you\'ve already checked in')
        else:
            print('Role not found')
        return
    
    # when check out
    if 'check out' in message.content:
        role = discord.utils.get(guild.roles, name='on shift')
        if role is not None:
            if role in member.roles:
                try:
                    print(f'{member} is checking out..')
                    sheet.check_out_staff(member.display_name)
                    await member.remove_roles(role)
                    await message.channel.send(f'{member.mention} you\'ve been checked out')
                except Exception as e:
                    print(e)
                    await message.channel.send(f'{member.mention} error occured')
            else:
                await message.channel.send(f'{member.mention} you\'re not checked in yet')
        else:
            print('Role not found')
        return
    
    # Default
    if discord.utils.get(message.guild.members, name='Kiosk Bot') in message.mentions:
        print('before coooking')
        await message.channel.send('What\'s cooking?')

@KB.event
async def on_member_join(member):
    # await member.create_dm()
    # await member.dm_channel.send(
    #     f'Hi {member.name}, welcome to {member.guild} server!'
    # ) 
    print(f'{member.name} has joined the {member.guild}')
    await member.guild.channel.send(f'Hi {member.name}, welcome to {member.guild} server!')


# This is the key that Discord provided for each bot
# This key doesn't work
KB.run('Njg2MzQ2NTYxNTQxNjM2MTE2.Xmr3tw.v3vmYcaso1hHMgP5NeM1uVVU_BE')