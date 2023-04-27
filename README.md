# Python-Telegram-Multibot

# Objective
Demonstrate how two telegram bot can work together to address much complicated usecase.

# Scenario
In this demonstration we assumen general-user had already signup to our `master bot` and admin-user uses `worker bot` to fire broadcast job.

# KISS
Since this is a over simplified example, I use local storage `members.txt` to represent a much complicated DB. But one important key is both master and worker should have access to this shared storage space. 

# Prerequisite
1. Get a Bot Token from BotFather, may refer to [site](https://help.zoho.com/portal/en/kb/desk/support-channels/instant-messaging/telegram/articles/telegram-integration-with-zoho-desk#Telegram_Integration)
1. Install Python if your computer don't have `Python` installed

# Reference
Any user of this repo should always refer to [official-site](https://docs.python-telegram-bot.org/en/stable/#telegram-api-support) for the most accurate information. At the point of writing, I refer to [v20.1](https://docs.python-telegram-bot.org/en/v20.1/). 

# Get Started
## Environment
\
OS: Ubuntu 22.04\
Python: Python 3.10.6\
PS: I suppose it will also work on Windows 11, but I haven't done it.

## Commands
\
Copy and run command below.
```
git clone git@github.com:JonahTzuChi/Python-Telegram-Multibot-Bot.git
```
```
cd Python-Telegram-Multibot-Bot
```
```
pip3 install -r requirements.txt
```
```
mv ./config/config-example.yml ./config/config.yml
nano ./config/config.yml
# update MASTER_TELEGRAM_TOKEN: "<TELEGRAM_TOKEN_1>"
# update WORKER_TELEGRAM_TOKEN: "<TELEGRAM_TOKEN_2>"