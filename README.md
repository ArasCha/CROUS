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

!city <string>
Displays the city name, residence name, rent amount and area size of the city corresponding to the string given

### !clear <nb>
Delete the last nb messages from the tchat

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
	- go the `src/` folder
	- `sudo touch .env`
	- `sudo nano .env`
	- Write in the necessary content (explained above)
	- Ctrl+o to save the file
	- Ctrl+x to exit the file

- Creating the environment:
	- `sudo python3 -m venv env`

- Activating the environment:
	- go in `/env/bin`
	- `source activate`

- Installing requirements:
	- Make sure you're in the Python environment (env)
	We have to use sudo to install packages with pip on this Rasp.
	But using sudo makes us going outside of the environment.
	We have to make sudo keeping us in the environment by using it.
	So we have to do what is said on this page:
	https://stackoverflow.com/questions/50335676/sudo-privileges-within-python-virtualenv
	- `sudo ./env/bin/python -m pip install -r requirements-dev.txt`

- Launching the program:
	- go in the `src/` folder
	- `sudo ../env/bin/python main.py`
