
#_______________.___.  __      __  _____  ____  ___
#\______   \__  |   | /  \    /  \/  _  \ \   \/  /
# |    |  _//   |   | \   \/\/   /  /_\  \ \     / 
# |    |   \\____   |  \        /    |    \/     \ 
# |______  // ______|   \__/\  /\____|__  /___/\  \
#        \/ \/               \/         \/      \_/


import discord
from discord import app_commands

from discord.ext import commands, tasks
import random

intents = discord.Intents().all()
bot = commands.Bot(command_prefix = "+", intents = intents)
bot.remove_command("help")
status = ["Prefix +",
          "Version : 1.0"]
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

intents = discord.Intents.default()
intents.typing = False
intents.presences = False


@bot.event
async def on_ready():
    print(f"{bot.user.name} bot open")
    changeStatus.start()


@bot.event
async def on_member_join(member):
    
    bienvenue = "**Bienvenue sur Lunar Network**"

    
    await member.send(bienvenue)
    print(f"Message envoyé à {member.name}")


@bot.command
async def start(ctx, secondes = 10):
    changeStatus.change_interval(sec = secondes)

@tasks.loop(seconds = 10)
async def changeStatus():
    game = discord.Game(random.choice(status))
    await bot.change_presence(status = discord.Status.dnd, activity = game)

@bot.command()
async def clear(ctx, amount=5):
    await ctx.message.delete()
    if ctx.message.author.guild_permissions.manage_messages:
        await ctx.channel.purge(limit=amount + 1)  
        await ctx.send(f'{amount} messages ont été **supprimés** par {ctx.author.mention}', delete_after=5)  
    else:
        await ctx.send("Vous n'avez pas la permission de gérer les messages.")


@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.ban_members:
        
        await member.ban(reason=reason)
        
        
        await ctx.send(f'{member.mention} a été **banni**. Raison : {reason}')
        
        
        if reason is not None:
            dm_message = f"Vous avez été banni par {ctx.author.display_name} pour la raison suivante : {reason}"
        else:
            dm_message = f"Vous avez été banni par {ctx.author.display_name} sans raison spécifiée."
        
        try:
            await member.send(dm_message)
        except discord.Forbidden:
            
            await ctx.send("Impossible d'envoyer un message en DM au membre banni (DM désactivés).")
    else:
        await ctx.send("Vous n'avez pas la permission de bannir des membres.")



@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await ctx.message.delete()
    if ctx.author.guild_permissions.kick_members:
        if member.guild_permissions.administrator:
            await ctx.send("Vous ne pouvez pas kicker un administrateur.")
        else:
            await member.kick(reason=reason)
            await ctx.send(f'{member.mention} a été **kick**.')
    else:
        await ctx.send("Vous n'avez pas la permission de kick des membres.")


@bot.command()
async def unban(ctx, *, member_id):
    await ctx.message.delete()
    if ctx.author.guild_permissions.ban_members:
        try:
            
            member = await bot.fetch_user(int(member_id))
            
            
            await ctx.guild.unban(member)
            
            
            await ctx.send(f'{member.name}#{member.discriminator} a été **débanni**.')
        except discord.NotFound:
            await ctx.send(f'Aucun utilisateur avec l\'ID {member_id} n\'a été trouvé.')
    else:
        await ctx.send('Vous n\'avez pas la permission de débanir des membres.')



@bot.command()
async def addrole(ctx, member: discord.Member, role: discord.Role):
    if role not in member.roles:
        await member.add_roles(role)
        await ctx.send(f"{role.name} a été ajouté à {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} a déjà le rôle {role.name}")


@bot.command()
async def removerole(ctx, member: discord.Member, role: discord.Role):
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"{role.name} a été retiré de {member.display_name}")
    else:
        await ctx.send(f"{member.display_name} n'a pas le rôle {role.name}")

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)
    print(f"Le Message envoyer : => {message}")

bot.run("MTE3NjI3MDY4MTUzMzU5MTU1Mg.GZbksW.s9X5GKSxitHKRnw8Z3Cv6BMe7ola19RSt4NGhw")