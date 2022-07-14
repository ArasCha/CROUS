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

## Information

The bot points out when the token is dead

## Start the program

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

### On the Sam's Rasp:


- Pulling:
	- Go in the `Aras` folder (home/Aras/):
	- `sudo git pull https://github.com/ArasCha/CROUS.git`
	- username: ArasCha
	- password: my GitHub token

- Creating the `.env` file:
	- `sudo touch .env`
	- `sudo nano .env`
	- Write the .env content.
	- Ctrl+o to save the file
	- Ctrl+x to exit the file

- Creating the environment:
	- `sudo python3 -m venv env`

- Activating the environment:
	- go in `/env/bin`
	- `source activate`

- Installing requirements:
	- `sudo pip install -r requirements-dev.txt`
	Using sudo makes us going outside of the environment
	So we have to do what is said on this page:
	https://superuser.com/questions/232231/how-do-i-make-sudo-preserve-my-environment-variables
- Launching the program:
	- `