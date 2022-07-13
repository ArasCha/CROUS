# CROUS
Bot which notifies me whether a CROUS accomodation is available

## Commands

### !status
See whether the bot is requesting the CROUS api

### !start
Make the bot doing requests (by default)

### !stop
Stop the bot from making requests

### !token <token_value>
Change token

### Information

The bot points out when the token is dead

### Start the program

Just after pulling the project:

- create a `.env` file in the `src` folder. Inside:
	- put the CROUS_TOKEN (the token of your messervices account)
	- put the DISCORD_BOT_TOKEN

- put yourself at the root of your project
	- do `python -m venv env`
	- activate the environment by launching `activate` in `env/Scripts`

- once in the Python environement, install requirements:
	- do `pip install -r requirements-dev.txt`

- still in the Python environment, launch the program:
	- do `python main.py` in the `src` folder