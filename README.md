# Infobot
[![GitHub](https://img.shields.io/github/license/InfobotOrg/infobot)](LICENSE)
![Lines of code](https://img.shields.io/tokei/lines/github/InfobotOrg/infobot)

This is a (romanian-only) Discord bot that can fetch data from sites such as [PbInfo](https://pbinfo.ro), [SolInfo](https://solinfo.ro) and [InfoArena](https://infoarena.ro).  
Link to add the bot to your server: [Bot Invite](https://discord.com/oauth2/authorize?client_id=1006240882812539043&permissions=2147485696&scope=bot).

## Config
For the project to start, a `.env` file is needed having to following fields:
- `TOKEN` - the discord api bot token

## Run
To run locally, you must have python 3.8 or higher (and pip) installed:
- `pip install -r requirements.txt`
- `python main.py`

Or run via docker:
- `docker build -t infobot .`
- `docker run -d -it --name=infobot infobot`
