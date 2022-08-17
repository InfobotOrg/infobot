# Infobot
This is a Discord bot that can fetch data from sites such as [PbInfo](https://pbinfo.ro), [SolInfo](https://solinfo.ro) and [InfoArena](https://infoarena.ro).  
[Add the bot to a server.](https://discord.com/oauth2/authorize?client_id=1006240882812539043&permissions=2147485696&scope=bot)

## Config
For the project to start, a `.env` file is needed having to following fields:
- `TOKEN` - the discord api bot token
- `GITHUB_TOKEN` - the github api token

## Run
To run locally, you must have python 3.8 or higher (and pip) installed:
- `pip install -r requirements.txt`
- `python main.py`

Or run via docker:
- `docker build -t infobot .`
- `docker run -d -it --name=infobot infobot`
