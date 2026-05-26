# chitato
A simple discord bot for polling a source server SDR address under a private network.

## Requirements
Since this bot was made for running under the same network as the srcds instances, a direct connection is required for this to work.
If your server has more than one NIC, make sure to bind the IP, so the bot can make the RCON calls by adding the following launch parameters:
`-usercon +ip adapter_ip -enablefakeip`

## Deployment
- Create a .env file using as an example `.env.example`
- Set up the required env variables: 
    - `TOKEN` : Discord bot token
    - `DISCORD_IP_INFO_CHANNEL_ID` : Discord channel ID where the info should be displayed 
- Configure the servers to poll via `servers.json` with its address and rcon password.
- Install the requirements via `pip install -r requirements.txt`
- Launch the bot: `python bot.py`

## TODO:
- Create a systemd unit to autostart the bot
- Add commands and fine tunning, error checking and other stuff.

## Troubleshooting
### Connection refused when executing a rcon command
Make sure to add `-usercon +ip adapter_ip` to the servers launch options. 
ex: `./srcds_run -console -game tf +map map_name +servercfgfile cfg_file.cfg +sv_pure 1 +maxplayers 24 +mapcyclefile mapcycle_custom.txt -port 27015 -usercon +ip 10.22.0.15 -enablefakeip`