import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GROUP_COUNT = 26
ROLES_PREFIX = "Grupo "

client = discord.Client(intents=discord.Intents.all())

def get_emoji_by_number(number):
    return {
        1: '๐ฆ',
        2: '๐ง',
        3: '๐จ',
        4: '๐ฉ',
        5: '๐ช',
        6: '๐ซ',
        7: '๐ฌ',
        8: '๐ญ',
        9: '๐ฎ',
        10: '๐ฏ',
        11: '๐ฐ',
        12: '๐ฑ',
        13: '๐ฒ',
        14: '๐ณ',
        15: '๐ด',
        16: '๐ต',
        17: '๐ถ',
        18: '๐ท',
        19: '๐ธ',
        20: '๐น',
        21: '๐บ',
        22: '๐ป',
        23: '๐ผ',
        24: '๐ฝ',
        25: '๐พ',
        26: '๐ฟ'
    }.get(number, None)

async def create_group(guild, group_number):
    category_name = f"{ROLES_PREFIX}{group_number}"
    category_channel = discord.utils.get(guild.categories, name=category_name)
    if category_channel is None:
        category_channel = await guild.create_category(name=category_name)
        await category_channel.create_voice_channel(f"{ROLES_PREFIX}{group_number} / Estudiando")
        await category_channel.create_text_channel(f"{ROLES_PREFIX}{group_number} / General")
        await category_channel.create_text_channel(f"{ROLES_PREFIX}{group_number} / Notas-Recursos")
        print(f"Categorรญa del grupo {group_number} creada")
    else:
        print(f"Categorรญa del grupo {group_number} ya existe")
    return category_channel

async def assign_role(payload, message_id):
    guild = client.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)
    emoji_number = ord(str(payload.emoji)) - ord('๐ฆ') + 1
    if 1 <= emoji_number <= GROUP_COUNT:
        role = discord.utils.get(guild.roles, name=f"{ROLES_PREFIX}{emoji_number}")
        existing_roles = [r for r in member.roles if r.name.startswith(ROLES_PREFIX)]
        if existing_roles:
            await member.remove_roles(*existing_roles)
            print(f"Roles {', '.join([r.name for r in existing_roles])} removidos de {member.name}")
        await member.add_roles(role)
        print(f"Rol {role.name} asignado a {member.name}")
    else:
        print(f"No se encontrรณ el rol para el emoji {payload.emoji}")
    message = await client.get_channel(payload.channel_id).fetch_message(message_id)
    await message.remove_reaction(payload.emoji, member)



@client.event
async def on_ready():
    print(f'{client.user.name} se ha conectado al Discord!')
    guild = discord.utils.get(client.guilds, name=GUILD)
    if guild is None:
        print(f"No se encontrรณ el servidor '{GUILD}'.")
        return
    print(f"{guild.name} (id: {guild.id})")

    # Obtener el canal y el mensaje
    channel = await client.fetch_channel(int(os.getenv('channel_id')))
    message = await channel.fetch_message(int(os.getenv('message_id')))

    # Agregar reacciones al mensaje
    for i in range(1, GROUP_COUNT + 1):
        emoji = get_emoji_by_number(i)
        await message.add_reaction(emoji)


@client.event
async def on_raw_reaction_add(payload):
    channel = await client.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(int(os.getenv('message_id')))
    await assign_role(payload, message.id)

client.run(TOKEN)