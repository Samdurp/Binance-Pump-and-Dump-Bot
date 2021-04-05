# Binance-Pump-and-Dump-Bot

This bot will use a Discord bot to get a crypto currency name from Discord (signaled by a $) and place it into a txt file. The Python bot, which is run in parallel with the Javascript one, will take the crypto currency name output from the Javascript bot and use that as input, buying currency at the price and quantity specified by the user, and placing sell orders at either a minimum or maximum price for the crypto.

To use:
- Inside main.py, change variables to have the bot behave as you wish. Each one is commented so you can see what they do.
- Input your Binance.com (NOT BINANCE.US) public and private keys into the relevant fields in main.py
- Input your Discord user token and ownerID in config.json in the "config" folder.
- Run "MONEY.bat" (NOT "run.bat"), and then the Discord bot will scan for '$' characters. Once it finds one, it outputs it to output.txt. The rest is up to the python bot!

Javascript bot created by [TheRacingLion](https://github.com/TheRacingLion) and edited by Brendan Jones

Python bot by me!
