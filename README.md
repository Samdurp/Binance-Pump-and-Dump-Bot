# Binance-Pump-and-Dump-Bot

This bot will use a Discord bot to get a crypto currency name from Discord (signaled by a $) and place it into a txt file. The Python bot, which is run in parallel with the Javascript one, will take the crypto currency name output from the Javascript bot and use that as input, buying currency at the price and quantity specified by the user, and placing sell orders at either a minimum or maximum price for the crypto.

Please excuse the rough/inappropriate variable names. This project was very quickly thrown together in a week to take advantage of the then-popular pump and dump Discord servers.

To use:
- Inside main.py, change variables to have the bot behave as you wish. Each one is commented so you can see what they do.
- Input your Binance.com (NOT BINANCE.US) public and private keys into the relevant fields in main.py
- Input your Discord user token and ownerID in config.json in the "config" folder.
- Run "MONEY.bat" (NOT "run.bat"), and then the Discord bot will scan for '$' characters. Once it finds one, it outputs what follows the '$' to output.txt. The rest is up to the python bot with your settings!
- To reuse, delete output.txt and re-run the bot!

Important options:
- **client** (line 92 & 93): Copy/paste your binance.com (NOT binance.us) public key inside of the quotes on line 92, and place your binance.com (NOT binance.us) private key inside of the quotes on line 93. This will link the bot to your binance.com account and allow it to make transactions on your behalf.
- **maxPulloutPercent** (line 92): The price CEILING, expressed in a percentage (but without the % symbol), where the bot will automatically sell the buyCoin that the user has in their binance account. Example: if 200 is inputted, the bot will auto-sell when the price of the coin has doubled from the price it was purchased at.
- **minPulloutPercent** (line 93): The price FLOOR, expressed in a percentage (but without the % symbol), where the bot will automatically sell the buyCoin that the user has in their binance account. Example: if 50 is inputted, the bot will auto-sell when the price of the coin has halved from the price it was purchased at.
- **useOutputTxt** (line 14): Set to 1 if you want the bot to get the coin you are buying from the JavaScript (Discord) bot, 0 if you want the user to be able to type the coin out during script runtime.
- **enableOrders** (line 70): Set to 1 if you want the bot to place REAL orders on binance.com, 0 if you do just want to test the bot (will not place practice/dummy orders; it will stop running after calculating max and minimum amounts purchasable)
- **waitTime** (line 81): The length (in seconds) of the period of time where the program will not execute a sell order after the initial buy has gone through. This is to stop the program from selling immediately due to a small, short-lived dip in price right after placing a buy order.

Javascript bot created by [TheRacingLion](https://github.com/TheRacingLion) and edited by Brendan Jones

Python bot by me!

NOTE: This is a Discord selfbot. It is against Discord's terms of service to use a selfbot. Use at your own risk. We are not responsible for any losses, including but not limited to a ban or suspension of binance.com and/or Discord accounts, nor any financial losses.
