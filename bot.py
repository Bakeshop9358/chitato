import os
import logging
import discord
from discord.ext import tasks, commands
from datetime import date, datetime
from server import ServersInfo
from dotenv import load_dotenv

logger = logging.getLogger("Chitato")
logging.basicConfig()
logger.setLevel("INFO")


load_dotenv()
TOKEN = os.environ["TOKEN"]
DISCORD_IP_INFO_CHANNEL_ID = os.environ["DISCORD_IP_INFO_CHANNEL_ID"]


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="?", description="", intents=intents)

serversInfo = ServersInfo()


@tasks.loop(seconds=30)
async def send_server_info():
    logger.info("looping server info")

    if not serversInfo.check_for_changes():
        logger.info("Las IPs no  han cambiado, omitiendo actualización")
        return

    server_info_content = serversInfo.get_servers_info()

    channel = bot.get_channel(int(DISCORD_IP_INFO_CHANNEL_ID))
    msg = None


    try:
        msg = await channel.fetch_message(channel.last_message_id)
    except Exception as e:
        logger.info(e)
        logger.info("No existe un último mensaje en el canal")
    if not msg:
        msg = await channel.send(server_info_content)
    else:
        await msg.edit(content=server_info_content)


@bot.event
async def on_ready():
    print(f"{bot.user} bot is ready")
    send_server_info.start()


bot.run(TOKEN)
